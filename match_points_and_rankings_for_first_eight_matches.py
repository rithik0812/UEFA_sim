import numpy as np

def assign_points_and_get_rankings(
    pairings,
    outcome_dist_lookupTable,
    team_symbols
):
    """
    Assigns points to teams based on pairings and outcome distributions, then returns sorted rankings.

    Parameters:
    - pairings: List of tuples representing team pairings (e.g., [('TeamA', 'TeamB'), ...]).
    - outcome_dist_lookupTable: Dictionary mapping team pairs to a tuple of probabilities
                                 (P(team1 wins), P(draw), P(team2 wins)).
    - team_symbols: List of team identifiers (e.g., ['TeamA', 'TeamB', ...]).

    Returns:
    - A dictionary of team symbols sorted by their total points in descending order.
    """
    
    # Step 1: Initialize points dictionary
    points_dict = {team: 0 for team in team_symbols}

    # Step 2: Process each pairing
    for pair in pairings:
        
        # Lookup the outcome distribution for the current pair
        outcome = outcome_dist_lookupTable.get(pair)
        
        if outcome is None:
            print(f"Pair {pair} not found in lookup table")
            continue
        
        # Sample from the multinomial distribution
        sample = np.random.multinomial(1, outcome)
        
        
        # Update points based on the sampled outcome
        if sample[0] == 1:
            # Team 1 wins
            points_dict[pair[0]] += 3
        elif sample[1] == 1:
            # Draw
            points_dict[pair[0]] += 1
            points_dict[pair[1]] += 1
        elif sample[2] == 1:
            # Team 2 wins
            points_dict[pair[1]] += 3

    # Sort the dictionary by points in descending order
    sorted_teams = sorted(points_dict.items(), key=lambda item: item[1], reverse=True)
    
    # Convert the sorted list back to a dictionary to maintain order
    sorted_points_dict = dict(sorted_teams)
    
    return sorted_points_dict


