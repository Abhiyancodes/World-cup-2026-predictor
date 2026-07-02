import random
from predict import load_model, predict_match

def simulate_single_match(team1, team2, model, elo, silent=False):
    _,probs = predict_match(team1, team2, neutral=1, model=model, elo=elo, silent=silent)

    outcomes = list(probs.keys())
    weights = list(probs.values())

    result = random.choices(outcomes, weights=weights, k=1)[0]

    if result==1:
        return team1
    elif result == -1:
        return team2
    else:
        return random.choice([team1, team2])
    
def simulate_knockout(teams, model, elo, round_name="Round", silent=False):
    if not silent:
        print("\n")
        print('=' * 50)
        print(round_name)
        print('=' * 50)
    
    winners = []
    for i in range(0, len(teams), 2):
        team1, team2 = teams[i], teams[i+1]
        winner = simulate_single_match(team1, team2, model, elo, silent=silent)
        if not silent:
            print(f"{team1:25} vs {team2:25} -> Winner : {winner}")
        winners.append(winner)
    
    return winners

if __name__ ==  "__main__":
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

    print(f"\n{'=' * 50}")
    print("ROUND OF 32 (fully simulated)")
    print('=' * 50)

    round32_winners = []
    for team1, team2 in round32_matchups:
        winner = simulate_single_match(team1, team2, model, elo)
        print(f"{team1:25} vs {team2:25} -> Winner : {winner}")
        round32_winners.append(winner)
    
    r16_winners = simulate_knockout(round32_winners, model, elo, "ROUND OF 16")
    qf_winners = simulate_knockout(r16_winners, model, elo, "QUARTERFINALS")
    sf_winners = simulate_knockout(qf_winners, model, elo, "SEMIFINALS")
    final_winners = simulate_knockout(sf_winners, model, elo, "FINAL")

    print("\n{'=' * 50}")
    print(f"CHAMPION : {final_winners[0]}")
    print('=' * 50)

