import pandas as pd

def prepare_data():
    df = pd.read_csv("data/results.csv")

    df = df[df['tournament'] != 'Friendly'].copy()

    def get_result(row):
        if row['home_score'] > row['away_score']:
            return 1
        elif row['home_score'] < row['away_score']:
            return -1
        else:
            return 0
        
    df['result'] = df.apply(get_result, axis=1)
    # similar to
    # for i in range(len(df)):
    #     row = df.iloc[i]
    #     df.at[i, 'result'] = get_result(row)


    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    print(f"Total Competitive Matches : {len(df)}")
    print("\nResult Distribution :")
    print(df['result'].value_counts()) 
    print("\nSample row : ")
    print(df[['date','home_team','away_team','home_score','away_score','result']].head(10))
     
    return df

if __name__ == "__main__":
    df = prepare_data()