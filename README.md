# Equity Pricing Tool

## Interactive quantitative finance app for pricing equity derivatives.

This project aims to develop a pricing tool for European options under the Black–Scholes model, including the calculation of Greeks, and subsequently extending it to support American, barrier, and Asian options, as well as binomial tree and Monte Carlo methods, along with an API and a web interface.

## Features
- European option pricing
- Black-Scholes model
- Greeks
- Interactive Streamlit interface
- Payoff vs current price chart

## 🚀 Live Demo

[![Open App](https://img.shields.io/badge/Open-App-2563eb?style=for-the-badge&logo=streamlit&logoColor=white)](https://equity-pricing-tool-uriellemm.streamlit.app/)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app/streamlit_app.py
