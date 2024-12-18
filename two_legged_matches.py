import numpy as np

def two_legged_sim(target_team, teams_9_to_24, average_goals_lookupTable, outcome_dist_lookupTable):
    """
    Simulates a two-legged match between target_team and its opponent.

    Parameters:
    - target_team (str): The team symbol for which the simulation is run (e.g., "ASV").
    - teams_9_to_24 (list): List of team symbols.
    - average_goals_lookupTable (dict): Mapping from team symbol to average goals per match.
    - outcome_dist_lookupTable (dict): Mapping from (team_a, team_b) to (prob_a_win, prob_draw, prob_b_win).

    Returns:
    - bool: True if target_team wins the aggregate score, False otherwise.
    """

    # Step 1: Determine Opponent Pairing
    n = len(teams_9_to_24)
    team_pairs = dict()
    for i in range(n // 2):
        team_a = teams_9_to_24[i]
        team_b = teams_9_to_24[-(i + 1)]
        team_pairs[team_a] = team_b
        team_pairs[team_b] = team_a

    opponent = team_pairs[target_team]

    # Step 2: Retrieve Outcome Probabilities
    pair_key = tuple(sorted((target_team, opponent)))

    prob_a_win, prob_draw_both, prob_b_win = outcome_dist_lookupTable[pair_key]

    # Step 3: Compute Custom Win Probabilities
    # For target_team
    prob_a_custom = prob_a_win + 0.5 * prob_draw_both
    # For opponent
    prob_b_custom = prob_b_win + 0.5 * prob_draw_both

    ratio_a_to_b = prob_a_custom / prob_b_custom
    ratio_b_to_a = prob_b_custom / prob_a_custom  

    # Step 5: Determine Lambda Values
    avg_goals_a = average_goals_lookupTable.get(pair_key[0])
    avg_goals_b = average_goals_lookupTable.get(pair_key[1])
    
    # the sim was showing extreme values so the following constraints:
    # min lambda = 1
    # max lambda = 3
    lambda_a = min(max(avg_goals_a * ratio_a_to_b, 1), 3) 
    lambda_b = min(max(avg_goals_b * ratio_b_to_a, 1), 3) 


    # Step 6: Simulate Two Legs
    # simulate the goals in the match by samples from poisson dist 
    # use the reletive strength ratio adjusted lambdas 
    total_goals_a = 0
    total_goals_b = 0
    legs = 2

    for leg in range(legs):
        goals_a = np.random.poisson(lam=lambda_a)
        goals_b = np.random.poisson(lam=lambda_b)
        total_goals_a += goals_a
        total_goals_b += goals_b
    
    # print(pair_key[0], pair_key[1])
    # print(lambda_a, lambda_b)
    # print (total_goals_a, total_goals_b)
    
    # Step 7: Determine Winner
    # depends on how it got sorted before
    if pair_key[0] == target_team:  
        return total_goals_a > total_goals_b
    else: 
        return total_goals_a < total_goals_b

