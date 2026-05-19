import streamlit as st


def hero_price_card(value: float, position: str, model: str, standard_error: float | None = None) -> None:
    se_text = "" if standard_error is None else f"<div class='hero-label'>MC Std. Error: {standard_error:.6f}</div>"
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-badge">{position.upper()} · {model.upper()}</div>
            <div class="hero-label">THEORETICAL VALUE</div>
            <div class="hero-value">{value:.4f}</div>
            {se_text}
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
