import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import numpy as np
import streamlit as st

from core.market import MarketData
from core.products import VanillaOption
from core.pricers.black_scholes import BlackScholesPricer
from core.pricers.binomial import BinomialPricer
from core.pricers.monte_carlo import MonteCarloPricer
from app.ui.styles import load_css
from app.ui.components import metric_card, hero_price_card
from app.ui.charts import payoff_vs_price_figure


st.set_page_config(
    page_title="Equity Derivatives Pricing Lab",
    page_icon="📈",
    layout="wide",
)

load_css()

st.markdown("<h1 class='title'>EQUITY DERIVATIVES PRICING LAB</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Black-Scholes · Binomial Tree · Monte Carlo</p>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.35], gap="large")

with left_col:
    st.markdown("<div class='panel-title'>PRODUCT</div>", unsafe_allow_html=True)

    exercise_style = st.selectbox("Exercise Style", ["european", "american", "bermudan"], index=0)
    option_type = st.radio("Option Type", ["call", "put"], horizontal=True)
    position = st.radio("Position", ["Long", "Short"], horizontal=True)

    bermudan_dates = 4
    if exercise_style == "bermudan":
        bermudan_dates = st.slider("Number of Bermudan exercise dates", min_value=1, max_value=24, value=4, step=1)

    if exercise_style == "european":
        available_models = ["Black-Scholes", "Binomial Tree", "Monte Carlo"]
    else:
        available_models = ["Binomial Tree", "Monte Carlo"]

    model_name = st.selectbox("Pricing Model", available_models)

    tree_steps = 250
    mc_paths = 10000
    mc_steps = 80
    mc_seed = 42

    if model_name == "Binomial Tree":
        tree_steps = st.slider("Tree Steps", min_value=25, max_value=1000, value=250, step=25)

    if model_name == "Monte Carlo":
        mc_paths = st.slider("Monte Carlo Paths", min_value=1000, max_value=100000, value=20000, step=1000)
        mc_steps = st.slider("Monte Carlo Time Steps", min_value=10, max_value=300, value=100, step=10)
        mc_seed = st.number_input("Random Seed", min_value=0, max_value=999999, value=42, step=1)

    st.markdown("<div class='panel-title'>MARKET AND CONTRACT PARAMETERS</div>", unsafe_allow_html=True)

    spot = st.slider("Spot S₀", min_value=10.0, max_value=300.0, value=100.0, step=1.0)
    strike = st.slider("Strike K", min_value=10.0, max_value=300.0, value=100.0, step=1.0)
    maturity = st.slider("Maturity T (years)", min_value=0.05, max_value=5.0, value=1.0, step=0.05)
    rate_pct = st.slider("Risk-free rate r (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.1)
    dividend_pct = st.slider("Dividend yield q (%)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
    vol_pct = st.slider("Volatility σ (%)", min_value=1.0, max_value=100.0, value=20.0, step=1.0)

rate = rate_pct / 100.0
dividend = dividend_pct / 100.0
volatility = vol_pct / 100.0

market = MarketData(spot, rate, dividend, volatility)
option = VanillaOption(strike, maturity, option_type, exercise_style, bermudan_dates)

try:
    if model_name == "Black-Scholes":
        result = BlackScholesPricer.price(option, market)
    elif model_name == "Binomial Tree":
        result = BinomialPricer.price(option, market, steps=tree_steps)
    else:
        result = MonteCarloPricer.price(option, market, paths=mc_paths, steps=mc_steps, seed=int(mc_seed))

except ValueError as exc:
    st.error(str(exc))
    st.stop()

sign = 1.0 if position == "Long" else -1.0
price = sign * result.price
delta = sign * result.delta
gamma = sign * result.gamma
theta = sign * result.theta
vega = sign * result.vega
rho = sign * result.rho

with right_col:
    hero_price_card(value=price, position=position, model=model_name, standard_error=result.standard_error)

    if model_name == "Monte Carlo":
        st.markdown(
            """
            <div class="info-box">
            Monte Carlo prices are statistical estimates. American and Bermudan options are handled with a simplified Longstaff-Schwartz regression algorithm.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if exercise_style == "american" and option_type == "put":
        st.markdown(
            """
            <div class="info-box">
            American puts may have early-exercise value. Numerical methods compare continuation value and immediate exercise value.
            </div>
            """,
            unsafe_allow_html=True,
        )

    greek_cols_1 = st.columns(3)
    greek_cols_2 = st.columns(2)

    with greek_cols_1[0]:
        metric_card("DELTA Δ", delta, accent="cyan")
    with greek_cols_1[1]:
        metric_card("GAMMA Γ", gamma, accent="orange")
    with greek_cols_1[2]:
        metric_card("THETA Θ", theta, accent="purple")
    with greek_cols_2[0]:
        metric_card("VEGA ν", vega, accent="green")
    with greek_cols_2[1]:
        metric_card("RHO ρ", rho, accent="yellow")

    chart_points = 120 if model_name == "Monte Carlo" else 220
    chart_mc_paths = min(mc_paths, 5000) if model_name == "Monte Carlo" else mc_paths
    s_grid = np.linspace(0.35 * strike, 2.1 * strike, chart_points)

    fig = payoff_vs_price_figure(
        s_grid=s_grid,
        strike=strike,
        maturity=maturity,
        rate=rate,
        dividend=dividend,
        volatility=volatility,
        option_type=option_type,
        exercise_style=exercise_style,
        bermudan_dates=bermudan_dates,
        current_spot=spot,
        position=position,
        model_name=model_name,
        tree_steps=tree_steps,
        mc_paths=chart_mc_paths,
        mc_steps=mc_steps,
        seed=int(mc_seed),
    )

    st.plotly_chart(fig, use_container_width=True)
