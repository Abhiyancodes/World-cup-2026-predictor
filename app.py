import sys
import os

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'src')
sys.path.insert(0, src_path)

from setup import setup
setup()

import streamlit as st
from predict import load_model, predict_match
from monte_carlo import run_monte_carlo

# Page Config
st.set_page_config(
    page_title="World Cup 2026 Predictor",
    page_icon="🏆",
    layout="centered"
)

st.title("World Cup 2026 Predictor")
st.markdown("Powered by Elo Ratings and Random Forest ML Model")
st.divider()

# Loading model and caching it
@st.cache_resource
def get_model():
    return load_model()

model, elo = get_model()
all_teams = sorted(elo.keys())

# Single Match Predictor
st.header("⚽ Single Match Predictor")
st.write("Pick any two teams and see who the model thinks will win.")

col1,col2 = st.columns(2)
with col1:
    home_team = st.selectbox("Home Team", all_teams, index=all_teams.index("Brazil"))
with col2:
    away_team = st.selectbox("Away Team", all_teams, index=all_teams.index("Portugal"))

neutral = st.checkbox("Neutral Venue (e.g. World Cup Match)", value=True)

if st.button("Predict Match", type="primary"):
    if home_team == away_team:
        st.warning("Please select two different teams!")
    else:
        predicted, probs = predict_match(
            home_team, away_team,
            neutral=int(neutral),
            model=model, elo=elo,
            silent=True
            )
        
        home_elo = elo.get(home_team, 1000)
        away_elo = elo.get(away_team, 1000)

        c1, c2 = st.columns(2)
        with c1:
            st.metric(f"{home_team} Elo rating", f"{home_elo:.0f}")
        with c2:
            st.metric(f"{away_team} Elo rating", f"{away_elo:.0f}")
        

        st.subheader("Prediction Probabilties")

        result_map = {1: "Home Win", 0: "Draw", -1: "Away Win"}
        colors = {1: "🟢", 0: "🟡", -1: "🔴"}

        for cls,label in result_map.items():
            pct = probs.get(cls, 0) * 100
            st.write(f"{colors[cls]} **{label}** -- {pct:.1f}%")
            st.progress(pct / 100)
        
        st.success(f"🏆 Predicted Champion : **{predicted}**")

st.divider()     

# Monte Carlo Championship Probabilities

st.header("🎲 Monte Carlo Championship Simulator")
st.write("Simulate the full World Cup 2026 (from Round of 32) bracket thousand of times to find the most likely champion.")

n_sims = st.slider("Number of Simulations", min_value=100, max_value=2000, value=500 ,step=100)

round32_matchups = [
    ("Canada",        "South Africa"),
    ("Brazil",        "Japan"),
    ("Germany",       "Paraguay"),
    ("Netherlands",   "Morocco"),
    ("Ivory Coast",   "Norway"),
    ("France",        "Sweden"),
    ("Mexico",        "Ecuador"),
    ("England",       "DR Congo"),
    ("Belgium",       "Senegal"),
    ("United States", "Bosnia and Herzegovina"),
    ("Spain",         "Austria"),
    ("Switzerland",   "Algeria"),
    ("Portugal",      "Croatia"),
    ("Australia",     "Egypt"),
    ("Argentina",     "Cape Verde"),
    ("Colombia",      "Ghana"),
]

if st.button("Run Monte Carlo Simulation", type="primary"):
    with st.spinner(f"Simulating {n_sims} tournaments..."):
        results = run_monte_carlo(round32_matchups, model, elo, n_simulations=n_sims)
    
    st.subheader("🏆 Championship Probailities")

    total = sum(results.values())

    for team, wins in results.most_common(15):
        pct = (wins / total) * 100
        st.write(f"**{team}** -- {pct:.1f}%")
        st.progress(pct / 100)

st.divider()
st.caption("Built with Python, Scikit-learn, Elo Ratings and Streamlit |  World Cup 2026")