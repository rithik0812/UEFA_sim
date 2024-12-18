from itertools import combinations

def compute_prob_tuple(team1, team2):
    """
    Compute the probability tuple for two teams based on their reltive strength.

    Parameters:
    - team1 (pd.Series): Row corresponding to the first team.
    - team2 (pd.Series): Row corresponding to the second team.

    Returns:
    - tuple: (prob_team1_wins, prob_draw, prob_team2_wins)
    """
        
    prob_team1_wins = round((team1['Win_prob'] + team2['Lose_prob']) / 2, 3)
    prob_draw = round((team1['Draw_prob'] + team2['Draw_prob']) / 2, 3)
    prob_team2_wins = round((team2['Win_prob'] + team1['Lose_prob']) / 2, 3)

    return (prob_team1_wins, prob_draw, prob_team2_wins)

def get_match_outcome_probs(df):
    """
    Create a dictionary mapping unique team pairs to their probability tuples.

    Parameters:
    - df (pd.DataFrame): DataFrame containing team symbols and their probabilities.

    Returns:
    - dict: Keys are sorted tuples of team symbols, values are probability tuples.
    """
    
    df_indexed = df.set_index('Team_Symbol')

    # Generate all unique pairs of team symbols using itertools.combinations
    team_pairs = [tuple(sorted(pair)) for pair in combinations(df_indexed.index, 2)]

    # Build the probability dictionary using dictionary comprehension
    prob_dict = {
        pair: compute_prob_tuple(
            df_indexed.loc[pair[0]],
            df_indexed.loc[pair[1]]
        )
        for pair in team_pairs
    }
    
    # print (prob_dict)
    return prob_dict

    