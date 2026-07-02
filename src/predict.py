import pickle
import pandas as pd

def load_model():
    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/elo_rating.pkl", "rb") as f:
        elo = pickle.load(f)
    return model, elo

def predict_match(home_team, away_team, neutral=1, model=None, elo=None, silent=False):
    if model is None and elo is None:
        model, elo = load_model()

    
    home_elo = elo.get(home_team, 1000)
    away_elo = elo.get(away_team, 1000)

    if not silent:
        if home_team not in elo:
            print(f"⚠️ '{home_team}' not found in Elo rating, using default 1000.")
        if away_team not in elo:
            print(f"⚠️ '{away_team}' not found in Elo rating, using default 1000.")

    X = pd.DataFrame([[home_elo, away_elo, neutral]],
                     columns=['home_elo','away_elo','neutral'])
    
    probs = model.predict_proba(X)[0] # gives you the confidence behind the answer in list of lists
    classes = model.classes_  # order of classes [-1, 0, 1]

    result_map = {1: "Home Win", 0: "Draw", -1: "Away Win"}

    if not silent:
        print(f"\n{home_team} (Elo : {home_elo:.0f}) vs {away_team} (Elo : {away_elo:.0f})") 
        print("-"*50)
        for cls, prob in zip(classes,probs):
            print(f"{result_map[cls]:12} -> {prob*100:.1f}%")
    
    predcted_class = model.predict(X)[0]
    if not silent:
        print(f"Predicted Result: {result_map[predcted_class]}")

    return result_map[predcted_class], dict(zip(classes, probs))

if __name__ == "__main__":
    predict_match("Brazil","Argentina", neutral=1)
    predict_match("Spain","Nepal", neutral=0)
    predict_match("France","England", neutral=1)


