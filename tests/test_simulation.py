import pytest
from ao_predictor.simulation import simulate_draw

def test_equal_players_have_approximately_equal_title_chances():
    result = simulate_draw(["A", "B"], {}, {}, n_simulations=12000, seed=7)
    a = result["players"]["A"]["title_probability"]
    b = result["players"]["B"]["title_probability"]
    assert a + b == pytest.approx(1.0)
    assert a == pytest.approx(0.5, abs=0.025)

def test_stronger_player_favored():
    overall = {"Strong": 1900, "Other": 1400}
    result = simulate_draw(["Strong", "Other"], overall, {}, n_simulations=5000, seed=11)
    assert result["players"]["Strong"]["title_probability"] > 0.9

def test_bye_advances_player():
    result = simulate_draw(["A", None, "B", "C"], {}, {}, n_simulations=100, seed=3)
    assert result["players"]["A"]["reach_Round of 2"] == 1.0

def test_seed_reproducible():
    first = simulate_draw(["A", "B", "C", "D"], {}, {}, n_simulations=200, seed=19)
    second = simulate_draw(["A", "B", "C", "D"], {}, {}, n_simulations=200, seed=19)
    assert first == second

def test_invalid_duplicate_draw_rejected():
    with pytest.raises(ValueError):
        simulate_draw(["A", "A"], {}, {})
