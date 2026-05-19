from core.market import MarketData
from core.products import VanillaOption
from core.pricers.binomial import BinomialPricer
from core.pricers.black_scholes import BlackScholesPricer


def test_american_put_more_valuable_than_european_put():
    market = MarketData(spot=100.0, rate=0.05, dividend=0.0, volatility=0.2)
    european_put = VanillaOption(100.0, 1.0, "put", "european")
    american_put = VanillaOption(100.0, 1.0, "put", "american")

    euro_price = BinomialPricer.price(european_put, market, steps=300).price
    amer_price = BinomialPricer.price(american_put, market, steps=300).price

    assert amer_price >= euro_price


def test_binomial_european_call_converges_to_black_scholes():
    market = MarketData(spot=100.0, rate=0.05, dividend=0.0, volatility=0.2)
    option = VanillaOption(100.0, 1.0, "call", "european")

    bs_price = BlackScholesPricer.price(option, market).price
    tree_price = BinomialPricer.price(option, market, steps=800).price

    assert abs(bs_price - tree_price) < 0.15


def test_bermudan_put_between_european_and_american_put():
    market = MarketData(spot=100.0, rate=0.05, dividend=0.0, volatility=0.2)
    euro = VanillaOption(100.0, 1.0, "put", "european")
    berm = VanillaOption(100.0, 1.0, "put", "bermudan", bermudan_dates=4)
    amer = VanillaOption(100.0, 1.0, "put", "american")

    euro_price = BinomialPricer.price(euro, market, steps=300).price
    berm_price = BinomialPricer.price(berm, market, steps=300).price
    amer_price = BinomialPricer.price(amer, market, steps=300).price

    assert euro_price <= berm_price <= amer_price
