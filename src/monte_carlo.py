from collections import Counter
from predict import load_model
from simulate_tournament import simulate_single_match, simulate_knockout

def run_single_simulation(round32_matchups, model, elo):
    round32_winners = []

    for team1,team2 in round32_matchups:
        winner = simulate_single_match(team1, team2, model, elo, silent=True )
        round32_winners.append(winner)

    r16_winners = simulate_knockout(round32_winners, model, elo, "", silent=True)
    qf_winners = simulate_knockout(r16_winners, model, elo, "", silent=True)
    sf_winners = simulate_knockout(qf_winners, model, elo, "", silent=True)
    final_winner = simulate_knockout(sf_winners, model, elo, "", silent=True)

    return final_winner[0]

def run_monte_carlo(round32_matchups , model, elo, n_simulations=1000,):
    champions = []

    print(f"Running {n_simulations} tournament simulations...")
    for i in range(n_simulations):
        if(i+1) % 100 == 0:
            print(f"{i+1}/{n_simulations} done...")
        champion = run_single_simulation(round32_matchups, model, elo)
        champions.append(champion)

    return Counter(champions)  # returns a dict of chamion counts

if __name__ == "__main__":
    model, elo = load_model()

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

    results = run_monte_carlo(round32_matchups, model, elo, n_simulations=1000)
    print(type(results))

    print(f"\n{'=' * 50}")
    print(f"WORLD CUP 2026 CHAMPION PROBABILITIES")
    print(f"BASED ON 1000 SIMULATIONS")
    print('=' * 50)


    # results (This is a dict) = Counter(champions) .most_common() gives the list of tuple in which first element of tuple is country and the second element is simulation champion
    for team, wins in results.most_common(): 
        pct = (wins/1000) * 100
        bar = '🟩' * int(pct/2) # visual bar
        print(f"{team:25} : {pct:5.1f}%   {bar}")