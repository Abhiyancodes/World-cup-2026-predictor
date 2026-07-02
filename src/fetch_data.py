import pandas as pd
import os

def fetch_data():
    url = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
    print("Downloading match data...")
    df = pd.read_csv(url)

    os.makedirs('data', exist_ok=True)
    df.to_csv('data/results.csv', index=False)
    print(f"{len(df)} matches saved to data/results.csv.")
    return df


if __name__ == "__main__":
    df = fetch_data()
    print(df.head())
    print(df.columns.to_list())

    