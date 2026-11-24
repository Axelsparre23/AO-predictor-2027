from .elo import expected_score, player_rating

def predict_match(player_a, player_b, overall, hard, hard_weight=0.35):
    ra = player_rating(player_a, overall, hard, hard_weight)
    rb = player_rating(player_b, overall, hard, hard_weight)
    pa = expected_score(ra, rb)
    return {"player_a": player_a, "player_b": player_b, "rating_a": round(ra, 1), "rating_b": round(rb, 1), "player_a_win_probability": pa, "player_b_win_probability": 1 - pa}
