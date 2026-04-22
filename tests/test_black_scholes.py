import math
from core.market import MarketData
from core.products import EuropeanOption
from core.pricers.black_scholes import BlackScholesPricer


def test_call_price_positive():
    market = MarketData(spot=100.0, rate=0.05, dividend=0.0, volatility=0.2)
    option = EuropeanOption(strike=100.0, maturity=1.0, option_type="call")

    result = BlackScholesPricer.price(option, market)

    assert result.price > 0.0


def test_put_price_positive():
    market = MarketData(spot=100.0, rate=0.05, dividend=0.0, volatility=0.2)
    option = EuropeanOption(strike=100.0, maturity=1.0, option_type="put")

    result = BlackScholesPricer.price(option, market)

    assert result.price > 0.0


def test_put_call_parity():
    market = MarketData(spot=100.0, rate=0.05, dividend=0.02, volatility=0.2)
    call = EuropeanOption(strike=100.0, maturity=1.0, option_type="call")
    put = EuropeanOption(strike=100.0, maturity=1.0, option_type="put")

    call_result = BlackScholesPricer.price(call, market)
    put_result = BlackScholesPricer.price(put, market)

    lhs = call_result.price - put_result.price
    rhs = market.spot * math.exp(-market.dividend * call.maturity) - call.strike * math.exp(-market.rate * call.maturity)

    assert abs(lhs - rhs) < 1e-10