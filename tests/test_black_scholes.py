import math

from core.market import MarketData
from core.products import VanillaOption
from core.pricers.black_scholes import BlackScholesPricer


def test_call_price_positive():
    market = MarketData(spot=100.0, rate=0.05, dividend=0.0, volatility=0.2)
    option = VanillaOption(strike=100.0, maturity=1.0, option_type="call", exercise_style="european")
    result = BlackScholesPricer.price(option, market)
    assert result.price > 0.0


def test_put_call_parity():
    market = MarketData(spot=100.0, rate=0.05, dividend=0.02, volatility=0.2)
    call = VanillaOption(strike=100.0, maturity=1.0, option_type="call", exercise_style="european")
    put = VanillaOption(strike=100.0, maturity=1.0, option_type="put", exercise_style="european")

    call_result = BlackScholesPricer.price(call, market)
    put_result = BlackScholesPricer.price(put, market)

    lhs = call_result.price - put_result.price
    rhs = market.spot * math.exp(-market.dividend * call.maturity) - call.strike * math.exp(-market.rate * call.maturity)

    assert abs(lhs - rhs) < 1e-10
