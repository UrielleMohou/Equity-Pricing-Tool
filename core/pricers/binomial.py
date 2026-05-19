import math

from core.market import MarketData
from core.products import VanillaOption
from core.results import PricingResult
from core.pricers.utils import intrinsic_value, bermudan_exercise_indices


class BinomialPricer:
    @staticmethod
    def price(option: VanillaOption, market: MarketData, steps: int = 250) -> PricingResult:
        option.validate()
        market.validate()

        price = BinomialPricer._price_only(option, market, steps)
        delta, gamma, theta = BinomialPricer._finite_difference_spot_time(option, market, steps)
        vega = BinomialPricer._finite_difference_vega(option, market, steps)
        rho = BinomialPricer._finite_difference_rho(option, market, steps)

        return PricingResult(price, delta, gamma, vega, theta, rho)

    @staticmethod
    def _price_only(option: VanillaOption, market: MarketData, steps: int) -> float:
        if steps < 1:
            raise ValueError("steps must be at least 1.")

        S0, K, T = market.spot, option.strike, option.maturity
        r, q, sigma = market.rate, market.dividend, market.volatility

        dt = T / steps
        u = math.exp(sigma * math.sqrt(dt))
        d = 1.0 / u
        disc = math.exp(-r * dt)
        p = (math.exp((r - q) * dt) - d) / (u - d)

        if not (0.0 < p < 1.0):
            raise ValueError("Risk-neutral probability is not in (0,1). Increase steps or check inputs.")

        option_values = []
        for j in range(steps + 1):
            s_t = S0 * (u ** j) * (d ** (steps - j))
            option_values.append(float(intrinsic_value(s_t, K, option.option_type)))

        exercise_indices = bermudan_exercise_indices(option, steps)

        for i in range(steps - 1, -1, -1):
            new_values = []
            can_exercise = i in exercise_indices
            for j in range(i + 1):
                s_ij = S0 * (u ** j) * (d ** (i - j))
                continuation = disc * (p * option_values[j + 1] + (1.0 - p) * option_values[j])
                if can_exercise:
                    exercise = float(intrinsic_value(s_ij, K, option.option_type))
                    new_values.append(max(continuation, exercise))
                else:
                    new_values.append(continuation)
            option_values = new_values

        return option_values[0]

    @staticmethod
    def _finite_difference_spot_time(option: VanillaOption, market: MarketData, steps: int):
        h_s = max(1e-2, 0.01 * market.spot)
        up = MarketData(market.spot + h_s, market.rate, market.dividend, market.volatility)
        down = MarketData(max(1e-8, market.spot - h_s), market.rate, market.dividend, market.volatility)

        v_up = BinomialPricer._price_only(option, up, steps)
        v_mid = BinomialPricer._price_only(option, market, steps)
        v_down = BinomialPricer._price_only(option, down, steps)

        delta = (v_up - v_down) / (2.0 * h_s)
        gamma = (v_up - 2.0 * v_mid + v_down) / (h_s ** 2)

        h_t = min(1e-3, 0.1 * option.maturity)
        if option.maturity <= h_t:
            theta = float("nan")
        else:
            shorter = VanillaOption(option.strike, option.maturity - h_t, option.option_type, option.exercise_style, option.bermudan_dates)
            v_short = BinomialPricer._price_only(shorter, market, steps)
            theta = (v_short - v_mid) / (-h_t)

        return delta, gamma, theta

    @staticmethod
    def _finite_difference_vega(option: VanillaOption, market: MarketData, steps: int) -> float:
        h = 1e-4
        up = MarketData(market.spot, market.rate, market.dividend, market.volatility + h)
        down = MarketData(market.spot, market.rate, market.dividend, max(1e-8, market.volatility - h))
        return (BinomialPricer._price_only(option, up, steps) - BinomialPricer._price_only(option, down, steps)) / (2.0 * h)

    @staticmethod
    def _finite_difference_rho(option: VanillaOption, market: MarketData, steps: int) -> float:
        h = 1e-4
        up = MarketData(market.spot, market.rate + h, market.dividend, market.volatility)
        down = MarketData(market.spot, market.rate - h, market.dividend, market.volatility)
        return (BinomialPricer._price_only(option, up, steps) - BinomialPricer._price_only(option, down, steps)) / (2.0 * h)
