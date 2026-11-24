import pandas as pd
import pytest
from ao_predictor.elo import expected_score, build_ratings
from ao_predictor.predict import predict_match
from ao_predictor.backtest import classification_metrics

def test_equal_ratings():
    assert expected_score(1500, 1500) == pytest.approx(0.5)

def test_higher_rating():
    assert expected_score(1600, 1500) > 0.5

def test_winner_rating_increases():
    data = pd.DataFrame([{"winner_name": "A", "loser_name": "B", "surface": "Hard"}])
    overall, hard = build_ratings(data)
    assert overall["A"] > 1500 and hard["A"] > 1500

def test_prediction_sums_to_one():
    data = pd.DataFrame([{"winner_name": "A", "loser_name": "B", "surface": "Hard"}])
    result = predict_match("A", "B", *build_ratings(data))
    assert result["player_a_win_probability"] + result["player_b_win_probability"] == pytest.approx(1)

def test_metrics():
    result = classification_metrics([0.9, 0.2], [1, 0])
    assert result["accuracy"] == 1 and result["n"] == 2
