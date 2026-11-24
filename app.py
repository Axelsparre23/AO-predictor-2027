from pathlib import Path
import streamlit as st
from ao_predictor.data import load_matches
from ao_predictor.elo import build_ratings
from ao_predictor.predict import predict_match

st.set_page_config(page_title="AO Predictor 2027", layout="wide")
st.title("AO Predictor 2027")
st.caption("Australian Open singles · Early model prototype")
tour = st.sidebar.selectbox("Tour", ["atp", "wta"], format_func=str.upper)

try:
    matches = load_matches(Path("data/raw"), tour)
    overall, hard = build_ratings(matches)
    st.success(f"{len(matches):,} matches loaded · Latest: {matches.tourney_date.max().date()}")
    players = sorted(set(matches.winner_name).union(matches.loser_name))
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
except FileNotFoundError as exc:
    st.warning(str(exc))
    st.write("Create data/raw/ and add ATP or WTA annual match CSV files. Sources are listed in README.")
