import random
import pandas as pd
import itertools

def generate_random_pairings_with_pots_df(
    df, 
    team_col='Team_Symbol', 
    pot_col='pot_number', 
    max_matches=8, 
    total_pairings=144, 
    matches_per_pot=2, 
    max_retries=1000
):
    """
    Generate pairings of teams from a pandas DataFrame with constraints:
    - Each team plays exactly `max_matches` matches.
    - Each team has exactly `matches_per_pot` matches against teams from each pot.
    - All pairings are unique (unordered).
    
    Parameters:
        df (pd.DataFrame): DataFrame containing team and pot information.
        team_col (str): Column name for team names.
        pot_col (str): Column name for pot identifiers.
        max_matches (int): The number of matches each team must play.
        total_pairings (int): The total number of unique pairings to generate.
        matches_per_pot (int): Number of matches each team has against each pot.
        max_retries (int): Maximum number of attempts to generate valid pairings.
        
    Returns:
        list: A list of unique pairings as tuples. Returns an empty list if failed.
    """
    
    pots = sorted(df[pot_col].unique())
    num_pots = len(pots)
    
    # Mapping from team to its pot
    team_to_pot = pd.Series(df[pot_col].values, index=df[team_col]).to_dict()
    
    # Create a mapping from pot to index
    pot_to_index = {pot: idx for idx, pot in enumerate(pots)}
    
    # List of all teams
    all_teams = list(team_to_pot.keys())
    
    # Precompute all possible unique pairings
    all_possible_pairings = list(itertools.combinations(all_teams, 2))
    
    for attempt in range(1, max_retries + 1):
        # print(f"Attempt {attempt}...")
        # Shuffle pairings to ensure randomness in each attempt
        random.shuffle(all_possible_pairings)
        
        # Initialize match counters
        match_counters = {team: 0 for team in all_teams}
        
        # Initialize pot_counters with tuples
        # Each tuple has a count corresponding to each pot index
        pot_counters = {team: tuple([0]*num_pots) for team in all_teams}
        
        pairings = set()
        
        for pair in all_possible_pairings:
            team_a, team_b = pair
            pot_a = team_to_pot[team_a]
            pot_b = team_to_pot[team_b]
            
            # Get pot indices
            pot_b_idx = pot_to_index[pot_b]
            pot_a_idx = pot_to_index[pot_a]
            
            # Current pot counts
            current_pot_a = pot_counters[team_a]
            current_pot_b = pot_counters[team_b]
            
            # Check if adding this pair violates any constraints
            if (
                match_counters[team_a] < max_matches and
                match_counters[team_b] < max_matches and
                current_pot_a[pot_b_idx] < matches_per_pot and
                current_pot_b[pot_a_idx] < matches_per_pot
            ):
                # Add the pair
                pair_sorted = tuple(sorted(pair))
                pairings.add(pair_sorted)
                
                # Update match counters
                match_counters[team_a] += 1
                match_counters[team_b] += 1
                
                # Update pot_counters by converting tuples to lists, incrementing, and converting back
                updated_pot_a = list(current_pot_a)
                updated_pot_a[pot_b_idx] += 1
                pot_counters[team_a] = tuple(updated_pot_a)
                
                updated_pot_b = list(current_pot_b)
                updated_pot_b[pot_a_idx] += 1
                pot_counters[team_b] = tuple(updated_pot_b)
                
                # Early exit if desired number of pairings is reached
                if len(pairings) == total_pairings:
                    # print("Reached 144 pairs")
                    break
        
        # After attempting to create pairings, validate constraints
        constraints_met = True
        for team in all_teams:
            if match_counters[team] != max_matches:
                constraints_met = False
                # print(f"Constraint failed: Team '{team}' has {match_counters[team]} matches, expected {max_matches}.")
                break
            for pot_idx, count in enumerate(pot_counters[team]):
                if count != matches_per_pot:
                    pot_name = pots[pot_idx]
                    constraints_met = False
                    # print(f"Constraint failed: Team '{team}' has {count} matches against Pot '{pot_name}', expected {matches_per_pot}.")
                    break
            if not constraints_met:
                break
        
        if constraints_met:
            # print(f"Successfully generated pairings on attempt {attempt}.")
            return list(pairings)
        else:
            # print(f"Attempt {attempt} failed. Retrying...")
            continue
    
    print(f"Failed to generate a valid set of pairings after {max_retries} attempts.")
    return []

