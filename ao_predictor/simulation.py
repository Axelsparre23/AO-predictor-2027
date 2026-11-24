from __future__ import annotations

import math
import numpy as np
from .elo import INITIAL_ELO, expected_score, player_rating

def simulate_draw(draw, overall, hard, n_simulations: int = 10000,
                  hard_weight: float = 0.35, seed: int | None = 42):
    """Simulate a single-elimination draw.

    draw is an ordered list of player names or None (an explicit bye).
    If its length is not a power of two, it is padded with byes at the end.
    The caller is responsible for supplying the real, correctly seeded draw.
    """
    if n_simulations < 1:
        raise ValueError("n_simulations must be at least 1")
    if len(draw) < 2:
        raise ValueError("draw must contain at least two slots")
    names = [p for p in draw if p is not None]
    if len(names) != len(set(names)):
        raise ValueError("each player may appear only once in the draw")
    if len(names) < 2:
        raise ValueError("draw must contain at least two named players")
    if any(not isinstance(p, str) or not p.strip() for p in names):
        raise ValueError("player names must be non-empty strings")

    size = 1 << math.ceil(math.log2(len(draw)))
    slots = list(draw) + [None] * (size - len(draw))
    n_rounds = int(math.log2(size))
    round_names = [f"Round of {size // (2 ** r)}" for r in range(n_rounds)]
    rng = np.random.default_rng(seed)
    reached = {name: np.zeros(n_rounds + 1, dtype=np.int64) for name in names}

    def win_probability(a, b):
        ra = player_rating(a, overall, hard, hard_weight) if a in overall or a in hard else INITIAL_ELO
        rb = player_rating(b, overall, hard, hard_weight) if b in overall or b in hard else INITIAL_ELO
        return expected_score(ra, rb)

    for _ in range(n_simulations):
        current = slots[:]
        for round_index in range(n_rounds):
            next_round = []
            for i in range(0, len(current), 2):
                a, b = current[i], current[i + 1]
                if a is None:
                    winner = b
                elif b is None:
                    winner = a
                else:
                    winner = a if rng.random() < win_probability(a, b) else b
                next_round.append(winner)
            for player in next_round:
                if player is not None:
                    reached[player][round_index + 1] += 1
            current = next_round

    players = {}
    for name, counts in reached.items():
        players[name] = {
            "reach_round_1": 1.0,
            **{f"reach_{round_names[i]}": float(counts[i + 1] / n_simulations)
               for i in range(n_rounds)},
            "title_probability": float(counts[-1] / n_simulations),
        }
    return {
        "simulations": n_simulations,
        "seed": seed,
        "rounds": round_names,
        "players": players,
    }
