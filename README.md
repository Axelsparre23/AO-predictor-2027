# AO Predictor 2027

Early MVP for forecasting the 2027 Australian Open men's and women's singles.

## Current scope
- Separate ATP and WTA historical data pipelines
- Overall and hard-court Elo ratings
- Head-to-head match win probabilities
- Evaluation metrics: accuracy, Brier score and log loss
- Streamlit interface

This is a baseline prototype, not a validated tournament forecast or betting advice. No player statistics are fabricated.

## Data
Download annual CSV files from:
- ATP: https://github.com/JeffSackmann/tennis_atp
- WTA: https://github.com/JeffSackmann/tennis_wta

Place files such as atp_matches_2026.csv and wta_matches_2026.csv in data/raw/. Missing data is reported rather than synthesized.

## Setup
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py

Run tests with: pytest

## Roadmap
1. Automated, provenance-tracked data updates
2. Serve/return and opponent-adjusted recent-form features
3. Injury, rest and fatigue data where reliable sources exist
4. Best-of-five ATP and best-of-three WTA match models
5. Chronological walk-forward backtesting and probability calibration
6. Monte Carlo draw simulations and title/round probabilities

Do not publish model performance claims until out-of-sample backtests are complete.
