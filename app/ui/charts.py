import math
import numpy as np
import plotly.graph_objects as go

from core.market import MarketData
from core.products import EuropeanOption
from core.pricers.black_scholes import BlackScholesPricer


def payoff_vector(s_grid: np.ndarray, strike: float, option_type: str) -> np.ndarray:
    if option_type == "call":
        return np.maximum(s_grid - strike, 0.0)
    return np.maximum(strike - s_grid, 0.0)


def price_vector(
    s_grid: np.ndarray,
    strike: float,
    maturity: float,
    rate: float,
    dividend: float,
    volatility: float,
    option_type: str,
) -> np.ndarray:
    prices = []

    for s in s_grid:
        market = MarketData(
            spot=float(s),
            rate=rate,
            dividend=dividend,
            volatility=volatility,
        )
        option = EuropeanOption(
            strike=strike,
            maturity=maturity,
            option_type=option_type,
        )
        result = BlackScholesPricer.price(option, market)
        prices.append(result.price)

    return np.array(prices)


def payoff_vs_price_figure(
    s_grid: np.ndarray,
    strike: float,
    maturity: float,
    rate: float,
    dividend: float,
    volatility: float,
    option_type: str,
    current_spot: float,
    position: str,
) -> go.Figure:
    payoff = payoff_vector(s_grid, strike, option_type)
    price = price_vector(
        s_grid=s_grid,
        strike=strike,
        maturity=maturity,
        rate=rate,
        dividend=dividend,
        volatility=volatility,
        option_type=option_type,
    )

    sign = 1.0 if position.lower() == "long" else -1.0
    payoff = sign * payoff
    price = sign * price

    current_idx = int(np.argmin(np.abs(s_grid - current_spot)))

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=s_grid,
            y=price,
            mode="lines",
            name="Current Price",
            line=dict(width=4, color="#36ddff"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=s_grid,
            y=payoff,
            mode="lines",
            name="Payoff at T",
            line=dict(width=3, color="#7c8ca8", dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[current_spot],
            y=[price[current_idx]],
            mode="markers",
            name="Current Spot",
            marker=dict(size=12, color="#36ddff"),
        )
    )

    fig.add_vline(
        x=current_spot,
        line_width=2,
        line_dash="solid",
        line_color="rgba(255,255,255,0.55)",
    )

    fig.update_layout(
        title="PRICE (T=0) VS PAYOFF (T) ",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(4,11,26,0.95)",
        font=dict(color="#cfe8ff"),
        hovermode="x unified",
        height=540,
        margin=dict(l=30, r=30, t=60, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="left",
            x=0.0,
        ),
    )

    fig.update_xaxes(
        title="Spot",
        gridcolor="rgba(130,160,210,0.18)",
        zeroline=False,
    )

    fig.update_yaxes(
        title="Value",
        gridcolor="rgba(130,160,210,0.18)",
        zeroline=False,
    )

    return fig