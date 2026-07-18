import pandas as pd
import pickle 
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

from prepare_data import prepare_data
from elo import compute_elo

def train():
    df = prepare_data()
    df, elo = compute_elo(df)

    # Features from which model learns and its target
    features = ['home_elo', 'away_elo', 'neutral']
    target = 'result'
    
    df['neutral'] = df['neutral'].astype(int)

    X = df[features]
    Y = df[target]

    le = LabelEncoder()
    y_encoded = le.fit_transform(Y)

    X_train, X_test, Y_train, Y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    print(f"\nTrainiing on {len(X_train)} matches.")
    print(f"Testing on {len(X_test)} matches.")

    model = xgb.XGBClassifier(
        n_estimators=100, 
        max_depth=4,
        learning_rate=0.1,
        objective="multi:softprob",
        eval_metric="mlogloss",
        num_class=3,
        random_state=42)
    
    model.fit(X_train, Y_train)

    Y_predi = model.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_predi)
    print(f"Model Accuracy : {accuracy * 100:.2f}%")


    os.makedirs("models", exist_ok=True)
    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("models/label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)
    with open("models/elo_rating.pkl", "wb") as f:
        pickle.dump(elo, f)
    
    print("\nModel saved to models/model.pkl")
    print("Label encoder saved to models/label_encoder.pkl")
    print("Elo ratings saved to models/elo_rating.pkl")

    return model, elo, le


if __name__ == "__main__":
    train()



