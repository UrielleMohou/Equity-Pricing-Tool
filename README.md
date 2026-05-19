# Equity Pricing Tool

## Interactive quantitative finance app for pricing equity derivatives.

This project aims to develop a pricing tool for European options under the Black–Scholes model, including the calculation of Greeks, and subsequently extending it to support American, barrier, and Asian options, as well as binomial tree and Monte Carlo methods, along with an API and a web interface.

## Features

- European option pricing with Black-Scholes closed-form formula
- European, American and Bermudan vanilla options with Cox-Ross-Rubinstein binomial tree
- European Monte Carlo pricing under geometric Brownian motion
- American and Bermudan Monte Carlo pricing with a simplified Longstaff-Schwartz algorithm
- Greeks computation with analytical formulas or finite differences depending on the method
- Interactive Streamlit dashboard with payoff and pricing visualization

## Method compatibility

| Exercise style | Black-Scholes | Binomial Tree | Monte Carlo |
|---|---:|---:|---:|
| European | Yes | Yes | Yes |
| American | No | Yes | Yes, Longstaff-Schwartz |
| Bermudan | No | Yes | Yes, Longstaff-Schwartz |

## 🚀 Live Demo

[![Open App](https://img.shields.io/badge/Open-App-2563eb?style=for-the-badge&logo=streamlit&logoColor=white)](https://equity-pricing-tool-uriellemm.streamlit.app/)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app/streamlit_app.py
