# It  is responsible for is the app ready to run (i.e. is model trained)
import os
import sys

from fetch_data import fetch_data
from prepare_data import prepare_data
from elo import compute_elo
from train_model import train

def setup():
    model_exists = os.path.exists("models/model.pkl")
    elo_exists = os.path.exists("models/elo_rating.pkl")
    data_exists = os.path.exists("data/results.csv")
    
    if not model_exists or not elo_exists:
        print("Model not found. Generating from scratch...")

        if not data_exists:
            print("Fetching data...")
            fetch_data()
        else:
            print("Data already exists, skipping fetch.")
        
        print("Preparing Data...")
        df = prepare_data()

        print("Computing Elo ratings...")
        df, _ = compute_elo(df)

        print("Training model...")
        train()

        print("Setup Completed!")
    else:
        print("Model found. Skipping setup.")

if __name__ == "__main__":
    setup()

