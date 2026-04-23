import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

import numpy as np
import streamlit as st

from core.market import MarketData
from core.products import EuropeanOption
from core.pricers.black_scholes import BlackScholesPricer
from app.ui.styles import load_css
from app.ui.components import metric_card, hero_price_card
from app.ui.charts import payoff_vs_price_figure


st.set_page_config(
    page_title="Options Lab",
    page_icon="📈",
    layout="wide",
)

load_css()

st.markdown("<h1 class='title'>OPTIONS LAB</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Equity Derivatives Pricing Toolkit</p>",
    unsafe_allow_html=True
)

# --- Top pseudo-tabs
product_cols = st.columns(6)
product_names = ["European", "American", "Barrier", "Digital", "Asian", "Basket"]

selected_product = "European"
for i, name in enumerate(product_names):
    with product_cols[i]:
        if st.button(name, use_container_width=True):
            selected_product = name

st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.25], gap="large")

with left_col:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>POSITION</div>", unsafe_allow_html=True)
    position = st.radio(
        "Position",
        ["Long", "Short"],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown("<div class='panel-title'>PARAMETERS</div>", unsafe_allow_html=True)

    spot = st.slider("Spot S₀", min_value=10.0, max_value=300.0, value=100.0, step=1.0)
    strike = st.slider("Strike K", min_value=10.0, max_value=300.0, value=100.0, step=1.0)
    maturity = st.slider("Maturity T (years)", min_value=0.05, max_value=5.0, value=1.0, step=0.05)
    rate_pct = st.slider("Rate r (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.1)
    dividend_pct = st.slider("Yield q (%)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
    vol_pct = st.slider("Vol σ (%)", min_value=1.0, max_value=100.0, value=20.0, step=1.0)

    option_type = st.radio(
        "Option Type",
        ["call", "put"],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown("</div>", unsafe_allow_html=True)

rate = rate_pct / 100.0
dividend = dividend_pct / 100.0
vol = vol_pct / 100.0

market = MarketData(
    spot=spot,
    rate=rate,
    dividend=dividend,
    volatility=vol,
)

option = EuropeanOption(
    strike=strike,
    maturity=maturity,
    option_type=option_type,
)

result = BlackScholesPricer.price(option=option, market=market)

sign = 1.0 if position == "Long" else -1.0

price = sign * result.price
delta = sign * result.delta
gamma = sign * result.gamma
theta = sign * result.theta
vega = sign * result.vega
rho = sign * result.rho

with right_col:
    hero_price_card(value=price, position=position)

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

    st.markdown("<div class='chart-block'>", unsafe_allow_html=True)

    s_grid = np.linspace(0.35 * strike, 2.1 * strike, 300)
    fig = payoff_vs_price_figure(
        s_grid=s_grid,
        strike=strike,
        maturity=maturity,
        rate=rate,
        dividend=dividend,
        volatility=vol,
        option_type=option_type,
        current_spot=spot,
        position=position,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)