from pathlib import Path
import streamlit as st
from ao_predictor.data import load_matches
from ao_predictor.elo import build_ratings
from ao_predictor.predict import predict_match
from ao_predictor.simulation import simulate_draw

st.set_page_config(page_title="AO Predictor 2027", layout="wide")
st.title("AO Predictor 2027")
st.caption("Australian Open singles · Early model prototype")
tour = st.sidebar.selectbox("Tour", ["atp", "wta"], format_func=str.upper)

try:
    matches = load_matches(Path("data/raw"), tour)
    overall, hard = build_ratings(matches)
    st.success(f"{len(matches):,} matches loaded · Latest: {matches.tourney_date.max().date()}")
    players = sorted(set(matches.winner_name).union(matches.loser_name))

    st.subheader("Match prediction")
    c1, c2 = st.columns(2)
    a = c1.selectbox("Player A", players)
    b = c2.selectbox("Player B", players, index=min(1, len(players)-1))
    if a == b:
        st.warning("Select two different players.")
    else:
        result = predict_match(a, b, overall, hard)
        x, y = st.columns(2)
        x.metric(f"{a} win probability", f"{result['player_a_win_probability']:.1%}")
        y.metric(f"{b} win probability", f"{result['player_b_win_probability']:.1%}")
        st.caption("Uncalibrated Elo baseline; not a tournament forecast.")

    st.divider()
    st.subheader("Tournament simulation")
    st.caption("Choose the entrants in their intended bracket order. This is a user-entered test draw, not the official AO 2027 draw.")
    entrants = st.multiselect("Draw entrants", players, max_selections=128)
    simulations = st.number_input("Monte Carlo simulations", min_value=1000, max_value=100000, value=10000, step=1000)
    seed = st.number_input("Random seed", min_value=0, value=42, step=1)
    if st.button("Simulate draw", disabled=len(entrants) < 2):
        result = simulate_draw(entrants, overall, hard, int(simulations), seed=int(seed))
        rows = []
        for name, probabilities in result["players"].items():
            rows.append({"Player": name, **{key.replace("reach_", "Reach "): value for key, value in probabilities.items()}})
        table = __import__("pandas").DataFrame(rows).sort_values("title_probability", ascending=False)
        st.dataframe(table, use_container_width=True, hide_index=True)
        st.caption(f"{result['simulations']:,} simulations · seed {result['seed']}. Probabilities depend on the entered order and Elo-only model.")
except FileNotFoundError as exc:
    st.warning(str(exc))
    st.write("Create data/raw/ and download ATP or WTA annual match CSV files using scripts/download_data.py. See README for instructions.")
