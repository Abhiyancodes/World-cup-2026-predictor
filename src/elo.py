import pandas as pd

def compute_elo(df, k=30, initial=1000):
    elo = {}  # stores current elo for every team

    home_elos = []  # elo of home team before the match
    away_elos = []  # elo of away team before the match

    for _, row in df.iterrows():
        home = row['home_team']
        away = row['away_team']

        if home not in elo:
            elo[home] = initial
        if away not in elo:
            elo[away] = initial

        home_elo = elo[home]
        away_elo = elo[away]

        # Saving before the match
        home_elos.append(home_elo)
        away_elos.append(away_elo)

        # Expected win probabulity using Elo formula
        x = (away_elo - home_elo)/400
        expected_home = 1 / (1 + 10 ** x)
        expected_away = 1 - expected_home

        # Actual result 
        if row['result'] == 1:
            actual_home, actual_away = 1, 0
        elif row['result'] == -1:
            actual_home, actual_away = 0, 1
        else:
            actual_home , actual_away = 0.5, 0.5 
        
        # Update elo after match
        elo[home] = home_elo + k * (actual_home - expected_home)
        elo[away] = away_elo + k * (actual_away - expected_away)

    df['home_elo'] = home_elos
    df['away_elo'] = away_elos

    return df,elo
    
if __name__ == "__main__":
    from prepare_data import prepare_data

    df = prepare_data()
    df, final_elo = compute_elo(df)

    print("\nSample with Elo ratings: ")
    print(df[['home_team', 'away_team', 'home_elo', 'away_elo', 'result']].tail(5))

    print("\nTop 10 strongest teams right now:")
    top10 = sorted(final_elo.items(), key=lambda x:x[1], reverse=True)[:10]
    for team, rating in top10:
     print(f" {team} : {rating:.0f}")





