# AO Predictor 2027

An evolving data-driven project for forecasting the 2027 Australian Open men's and women's singles. The current model is an Elo baseline with a Monte Carlo knockout-draw simulator.

## Implemented
- Separate ATP and WTA historical match CSV ingestion.
- Download script for public annual match datasets, with source URLs and UTC download timestamps recorded in a manifest.
- Overall Elo and hard-court Elo ratings.
- Head-to-head match win probabilities.
- Monte Carlo single-elimination draw simulation, including byes, advancement probabilities and title probabilities.
- Accuracy, Brier score and log-loss metric utility.
- Streamlit dashboard for match predictions and user-entered test draws.
- Unit tests for core model, data loader and simulator behavior.

## Important limitations
This is not yet a validated Australian Open 2027 forecast. The current Elo model is uncalibrated and does not yet account for serve/return matchups, recent form, injuries, withdrawals, fatigue, weather, or the ATP best-of-five versus WTA best-of-three format. The simulator uses the order of entrants exactly as entered; it does not know the official draw or seeding. Do not treat outputs as betting advice. No player entries, injuries, match data or performance results are fabricated.

## Data sources and download
Historical match results are from the public Jeff Sackmann datasets:
- ATP: https://github.com/JeffSackmann/tennis_atp
- WTA: https://github.com/JeffSackmann/tennis_wta

Install dependencies, then download the years you want. Example:

    python scripts/download_data.py --tour atp --years 2022 2023 2024 2025 2026
    python scripts/download_data.py --tour wta --years 2022 2023 2024 2025 2026

Files are saved in data/raw/ and download_manifest.json records each source URL and retrieval time. If a year is unavailable at the source, the script reports the HTTP error and does not create a fake file. Review dataset coverage before relying on predictions.

## Run locally

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py

Run tests:

    pytest

## Dashboard use
1. Select ATP or WTA.
2. Select two players for a baseline match probability.
3. For a draw simulation, select entrants in their intended bracket order.
4. Set the simulation count and random seed, then run the simulation.

The dashboard labels this as a user-entered test draw, not the official 2027 draw. For a non-power-of-two draw, remaining bracket positions are padded with byes at the end. Supply a correctly seeded and positioned draw before interpreting its probabilities.

## Model and evaluation roadmap
- Implement strict chronological walk-forward backtesting and probability calibration.
- Add opponent-adjusted recent form and serve/return features.
- Incorporate reliable rest/fatigue, injury and withdrawal information with source timestamps.
- Model ATP best-of-five and WTA best-of-three match formats.
- Obtain the official draw and simulate actual bracket advancement.
- Report sample size, accuracy, Brier score, log loss and calibration before making performance claims.

A passing unit test suite verifies code behavior, not predictive accuracy.
