import numpy as np
import plotly.graph_objects as go

from core.market import MarketData
from core.products import VanillaOption
from core.pricers.black_scholes import BlackScholesPricer
from core.pricers.binomial import BinomialPricer
from core.pricers.monte_carlo import MonteCarloPricer
from core.pricers.utils import intrinsic_value


def payoff_vector(s_grid: np.ndarray, strike: float, option_type: str) -> np.ndarray:
    return intrinsic_value(s_grid, strike, option_type)


def price_one(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    dividend: float,
    volatility: float,
    option_type: str,
    exercise_style: str,
    bermudan_dates: int,
    model_name: str,
    tree_steps: int,
    mc_paths: int,
    mc_steps: int,
    seed: int,
) -> float:
    market = MarketData(float(spot), rate, dividend, volatility)
    option = VanillaOption(strike, maturity, option_type, exercise_style, bermudan_dates)

    if model_name == "Black-Scholes":
        return BlackScholesPricer.price(option, market).price
    if model_name == "Binomial Tree":
        return BinomialPricer.price(option, market, steps=tree_steps).price
    return MonteCarloPricer.price(option, market, paths=mc_paths, steps=mc_steps, seed=seed, compute_greeks=False).price


def payoff_vs_price_figure(
    s_grid: np.ndarray,
    strike: float,
    maturity: float,
    rate: float,
    dividend: float,
    volatility: float,
    option_type: str,
    exercise_style: str,
    bermudan_dates: int,
    current_spot: float,
    position: str,
    model_name: str,
    tree_steps: int,
    mc_paths: int,
    mc_steps: int,
    seed: int,
) -> go.Figure:
    payoff = payoff_vector(s_grid, strike, option_type)

    prices = np.array([
        price_one(
            s,
            strike,
            maturity,
            rate,
            dividend,
            volatility,
            option_type,
            exercise_style,
            bermudan_dates,
            model_name,
            tree_steps,
            mc_paths,
            mc_steps,
            seed,
        )
        for s in s_grid
    ])

    sign = 1.0 if position.lower() == "long" else -1.0
    payoff = sign * payoff
    prices = sign * prices

    current_idx = int(np.argmin(np.abs(s_grid - current_spot)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=s_grid, y=prices, mode="lines", name="Current Price", line=dict(width=4, color="#36ddff")))
    fig.add_trace(go.Scatter(x=s_grid, y=payoff, mode="lines", name="Payoff at Maturity", line=dict(width=3, color="#7c8ca8", dash="dash")))
    fig.add_trace(go.Scatter(x=[current_spot], y=[prices[current_idx]], mode="markers", name="Current Spot", marker=dict(size=12, color="#36ddff")))

    fig.add_vline(x=current_spot, line_width=2, line_dash="solid", line_color="rgba(255,255,255,0.55)")

    fig.update_layout(
        title="PRICE TODAY VS PAYOFF AT MATURITY",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(4,11,26,0.95)",
        font=dict(color="#cfe8ff"),
        hovermode="x unified",
        height=520,
        margin=dict(l=30, r=30, t=60, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="left", x=0.0),
    )

    fig.update_xaxes(title="Spot", gridcolor="rgba(130,160,210,0.18)", zeroline=False)
    fig.update_yaxes(title="Value", gridcolor="rgba(130,160,210,0.18)", zeroline=False)
    return fig
