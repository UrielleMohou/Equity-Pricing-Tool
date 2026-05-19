from core.market import MarketData
from core.products import VanillaOption
from core.pricers.black_scholes import BlackScholesPricer
from core.pricers.monte_carlo import MonteCarloPricer


def test_monte_carlo_european_call_close_to_black_scholes():
    market = MarketData(spot=100.0, rate=0.05, dividend=0.0, volatility=0.2)
    option = VanillaOption(100.0, 1.0, "call", "european")

    bs = BlackScholesPricer.price(option, market).price
    mc = MonteCarloPricer.price(option, market, paths=30000, steps=60, seed=123, compute_greeks=False).price

    assert abs(bs - mc) < 0.6


def test_monte_carlo_american_put_positive():
    market = MarketData(spot=100.0, rate=0.05, dividend=0.0, volatility=0.2)
    option = VanillaOption(100.0, 1.0, "put", "american")

    result = MonteCarloPricer.price(option, market, paths=8000, steps=50, seed=123, compute_greeks=False)

    assert result.price > 0.0
