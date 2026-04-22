import streamlit as st


def hero_price_card(value: float, position: str) -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-badge">{position.upper()}</div>
            <div class="hero-label">THEORETICAL VALUE</div>
            <div class="hero-value">{value:.3f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: float, accent: str = "cyan") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value accent-{accent}">{value:.4f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )