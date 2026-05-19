import math

from core.market import MarketData
from core.products import VanillaOption
from core.results import PricingResult
from core.pricers.utils import normal_cdf, normal_pdf


def compute_d1_d2(market: MarketData, option: VanillaOption) -> tuple[float, float]:
    S = market.spot
    K = option.strike
    T = option.maturity
    r = market.rate
    q = market.dividend
    sigma = market.volatility

    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    return d1, d2


class BlackScholesPricer:
    @staticmethod
    def price(option: VanillaOption, market: MarketData) -> PricingResult:
        option.validate()
        market.validate()

        if option.exercise_style != "european":
            raise ValueError("Black-Scholes closed-form only supports European vanilla options.")

        S = market.spot
        K = option.strike
        T = option.maturity
        r = market.rate
        q = market.dividend
        sigma = market.volatility

        d1, d2 = compute_d1_d2(market, option)

        discount_r = math.exp(-r * T)
        discount_q = math.exp(-q * T)
        pdf_d1 = normal_pdf(d1)

        if option.option_type == "call":
            price = S * discount_q * normal_cdf(d1) - K * discount_r * normal_cdf(d2)
            delta = discount_q * normal_cdf(d1)
            theta = (
                -S * discount_q * pdf_d1 * sigma / (2.0 * math.sqrt(T))
                - r * K * discount_r * normal_cdf(d2)
                + q * S * discount_q * normal_cdf(d1)
            )
            rho = K * T * discount_r * normal_cdf(d2)
        else:
            price = K * discount_r * normal_cdf(-d2) - S * discount_q * normal_cdf(-d1)
            delta = discount_q * (normal_cdf(d1) - 1.0)
            theta = (
                -S * discount_q * pdf_d1 * sigma / (2.0 * math.sqrt(T))
                + r * K * discount_r * normal_cdf(-d2)
                - q * S * discount_q * normal_cdf(-d1)
            )
            rho = -K * T * discount_r * normal_cdf(-d2)

        gamma = discount_q * pdf_d1 / (S * sigma * math.sqrt(T))
        vega = S * discount_q * pdf_d1 * math.sqrt(T)

        return PricingResult(price, delta, gamma, vega, theta, rho)
