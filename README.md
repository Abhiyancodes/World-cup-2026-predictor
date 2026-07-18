# 🏆 World Cup 2026 Predictor

A machine learning based match predictor and tournament simulator for FIFA World Cup 2026, built using Elo ratings and a Random Forest classifier.

## 📌 Features
- **Single Match Predictor** — predict the outcome of any international match with win/draw/loss probabilities
- **Tournament Simulator** — simulate the full World Cup 2026 bracket
- **Monte Carlo Simulation** — run 1000+ simulations to find the most likely champion

## 🧠 How it works
1. Historical match data (50,000+ matches) fetched from [martj42/international_results](https://github.com/martj42/international_results)
2. Elo ratings computed for every team based on match history
3. Random Forest classifier trained on Elo features to predict match outcomes
4. Monte Carlo simulation runs the full bracket thousands of times

> **📝 Note:** Friendly matches are excluded from training data as they don't reflect true team strength as teams experiment with lineups, rest star players and don't play competitively. Only competitive matches (World Cup, qualifiers, continental tournaments) are used.

## 📁 Project Structure

```
World-cup-2026-predictor/
├── src/
│   ├── fetch_data.py          # Downloads match data
│   ├── prepare_data.py        # Cleans data, creates result labels
│   ├── elo.py                 # Computes Elo ratings for all teams
│   ├── train_model.py         # Trains Random Forest model
│   ├── predict.py             # Predicts match outcomes
│   ├── simulate_tournament.py # Simulates knockout bracket
│   └── monte_carlo.py         # Runs 1000 tournament simulations
├── app.py                     # Streamlit web app
├── requirements.txt           # Required libraries
└── .gitignore                 # Files excluded from git
```

## 🚀 How to run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Fetch data and train model
```bash
python src/fetch_data.py
python src/prepare_data.py
python src/train_model.py
```

### 3. Run the Streamlit app
```bash
streamlit run app.py
```

## 📊 Model Performance
- **Algorithm**: Random Forest Classifier
- **Training data**: 24,884 competitive international matches
- **Test accuracy**: 53.24%
- **Features**: Home Elo, Away Elo, Neutral venue

> **🔬 Experiment:** An XGBoost classifier was tested on the `xgboost` branch achieving **58.69% accuracy** (+5.45% improvement over Random Forest). Head over to the xgboost branch to check it out.

## 🏆 World Cup 2026 Prediction (1000 simulations)
| Team | Win Probability |
|------|----------------|
| England | 13.8% |
| Spain | 11.8% |
| France | 10.3% |
| Argentina | 9.2% |
| Japan | 7.8% |
| Germany | 5.8% |
| Portugal | 5.5% |
| Mexico | 5.5% |
| United States | 4.8% |
| Belgium | 3.5% |
| Morocco | 3.4% |
| Australia | 2.2% |
| Ecuador | 2.2% |
| Colombia | 2.1% |
| Brazil | 1.7% |

## 💡 Key Concepts Used
- **Elo Rating System** — self correcting belief system that updates team strength after every match based on expected vs actual result
- **Random Forest Classifier** — ensemble of 100 decision trees voting together for stable predictions
- **Monte Carlo Simulation** — running the tournament 1000 times with weighted random sampling to get true championship probabilities
- **Data Leakage Prevention** — Elo ratings saved before each match, not after, to prevent the model from cheating

## 🛠️ Built With
- Python 3.13
- Pandas & NumPy
- Scikit-learn
- Streamlit
- Elo Rating System

## 👤 Author
**Abhiyan Pathak** — [abhiyanpathak.com.np](https://abhiyanpathak.com.np) | [GitHub](https://github.com/Abhiyancodes)