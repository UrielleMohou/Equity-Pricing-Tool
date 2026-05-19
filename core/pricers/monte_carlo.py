import math
import numpy as np

from core.market import MarketData
from core.products import VanillaOption
from core.results import PricingResult
from core.pricers.utils import intrinsic_value, bermudan_exercise_indices


class MonteCarloPricer:
    @staticmethod
    def price(
        option: VanillaOption,
        market: MarketData,
        paths: int = 20000,
        steps: int = 100,
        seed: int | None = 42,
        compute_greeks: bool = True,
    ) -> PricingResult:
        option.validate()
        market.validate()

        price, se = MonteCarloPricer._price_only(option, market, paths, steps, seed)

        if not compute_greeks:
            return PricingResult(price, float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), se)

        delta, gamma, theta = MonteCarloPricer._finite_difference_spot_time(option, market, paths, steps, seed)
        vega = MonteCarloPricer._finite_difference_vega(option, market, paths, steps, seed)
        rho = MonteCarloPricer._finite_difference_rho(option, market, paths, steps, seed)

        return PricingResult(price, delta, gamma, vega, theta, rho, se)

    @staticmethod
    def _simulate_paths(market: MarketData, maturity: float, paths: int, steps: int, seed: int | None):
        if paths < 100:
            raise ValueError("paths should be at least 100.")
        if steps < 1:
            raise ValueError("steps must be at least 1.")

        rng = np.random.default_rng(seed)
        dt = maturity / steps
        z = rng.standard_normal((paths, steps))
        drift = (market.rate - market.dividend - 0.5 * market.volatility ** 2) * dt
        diffusion = market.volatility * math.sqrt(dt) * z
        log_returns = drift + diffusion

        log_paths = np.cumsum(log_returns, axis=1)
        stock_paths = market.spot * np.exp(log_paths)
        stock_paths = np.concatenate([np.full((paths, 1), market.spot), stock_paths], axis=1)
        return stock_paths

    @staticmethod
    def _price_only(option: VanillaOption, market: MarketData, paths: int, steps: int, seed: int | None):
        if option.exercise_style == "european":
            return MonteCarloPricer._price_european(option, market, paths, steps, seed)
        return MonteCarloPricer._price_lsm(option, market, paths, steps, seed)

    @staticmethod
    def _price_european(option: VanillaOption, market: MarketData, paths: int, steps: int, seed: int | None):
        stock_paths = MonteCarloPricer._simulate_paths(market, option.maturity, paths, steps, seed)
        terminal = stock_paths[:, -1]
        payoffs = intrinsic_value(terminal, option.strike, option.option_type)
        discounted = np.exp(-market.rate * option.maturity) * payoffs
        price = float(np.mean(discounted))
        se = float(np.std(discounted, ddof=1) / math.sqrt(paths))
        return price, se

    @staticmethod
    def _price_lsm(option: VanillaOption, market: MarketData, paths: int, steps: int, seed: int | None):
        stock_paths = MonteCarloPricer._simulate_paths(market, option.maturity, paths, steps, seed)
        dt = option.maturity / steps
        disc = math.exp(-market.rate * dt)

        exercise_indices = sorted(bermudan_exercise_indices(option, steps))
        if steps not in exercise_indices:
            exercise_indices.append(steps)

        cashflows = intrinsic_value(stock_paths[:, -1], option.strike, option.option_type)
        exercise_time = np.full(paths, steps, dtype=int)

        for t in reversed(exercise_indices[:-1]):
            alive = exercise_time > t
            if not np.any(alive):
                continue

            spot_t = stock_paths[alive, t]
            exercise_value = intrinsic_value(spot_t, option.strike, option.option_type)
            itm = exercise_value > 0

            if np.sum(itm) < 5:
                continue

            alive_indices = np.where(alive)[0]
            itm_indices = alive_indices[itm]
            x = stock_paths[itm_indices, t] / option.strike

            discounted_future = cashflows[itm_indices] * np.exp(-market.rate * dt * (exercise_time[itm_indices] - t))

            basis = np.vstack([np.ones_like(x), x, x ** 2]).T
            coeffs, *_ = np.linalg.lstsq(basis, discounted_future, rcond=None)
            continuation = basis @ coeffs

            immediate = intrinsic_value(stock_paths[itm_indices, t], option.strike, option.option_type)
            exercise_now = immediate > continuation

            ex_indices = itm_indices[exercise_now]
            cashflows[ex_indices] = immediate[exercise_now]
            exercise_time[ex_indices] = t

        discounted_cashflows = cashflows * np.exp(-market.rate * dt * exercise_time)
        price = float(np.mean(discounted_cashflows))
        se = float(np.std(discounted_cashflows, ddof=1) / math.sqrt(paths))
        return price, se

    @staticmethod
    def _finite_difference_spot_time(option: VanillaOption, market: MarketData, paths: int, steps: int, seed: int | None):
        h_s = max(1e-2, 0.01 * market.spot)

        up = MarketData(market.spot + h_s, market.rate, market.dividend, market.volatility)
        down = MarketData(max(1e-8, market.spot - h_s), market.rate, market.dividend, market.volatility)

        v_up, _ = MonteCarloPricer._price_only(option, up, paths, steps, seed)
        v_mid, _ = MonteCarloPricer._price_only(option, market, paths, steps, seed)
        v_down, _ = MonteCarloPricer._price_only(option, down, paths, steps, seed)

        delta = (v_up - v_down) / (2.0 * h_s)
        gamma = (v_up - 2.0 * v_mid + v_down) / (h_s ** 2)

        h_t = min(1e-3, 0.1 * option.maturity)
        if option.maturity <= h_t:
            theta = float("nan")
        else:
            shorter = VanillaOption(option.strike, option.maturity - h_t, option.option_type, option.exercise_style, option.bermudan_dates)
            v_short, _ = MonteCarloPricer._price_only(shorter, market, paths, steps, seed)
            theta = (v_short - v_mid) / (-h_t)

        return delta, gamma, theta

    @staticmethod
    def _finite_difference_vega(option: VanillaOption, market: MarketData, paths: int, steps: int, seed: int | None):
        h = 1e-4
        up = MarketData(market.spot, market.rate, market.dividend, market.volatility + h)
        down = MarketData(market.spot, market.rate, market.dividend, max(1e-8, market.volatility - h))
        v_up, _ = MonteCarloPricer._price_only(option, up, paths, steps, seed)
        v_down, _ = MonteCarloPricer._price_only(option, down, paths, steps, seed)
        return (v_up - v_down) / (2.0 * h)

    @staticmethod
    def _finite_difference_rho(option: VanillaOption, market: MarketData, paths: int, steps: int, seed: int | None):
        h = 1e-4
        up = MarketData(market.spot, market.rate + h, market.dividend, market.volatility)
        down = MarketData(market.spot, market.rate - h, market.dividend, market.volatility)
        v_up, _ = MonteCarloPricer._price_only(option, up, paths, steps, seed)
        v_down, _ = MonteCarloPricer._price_only(option, down, paths, steps, seed)
        return (v_up - v_down) / (2.0 * h)
