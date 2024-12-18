import pandas as pd
import time
import team_fixtures as tm
import team_pairings_match_outcomes as oc
import match_points_and_rankings_for_first_eight_matches as mrk
import rankings_helpers as rkh
import two_legged_matches as ll



ASV_SIM_Meters = dict(
    Total_Runs=0,
    ASV_Qualified=0,
    ASV_Top_8=0,
    ASV_Top_16_to_24_enters_2_legged=0,
    ASV_25_and_below=0,
    ASV_Won_2_legged=0,
    ASV_Lost_2_legged=0,
    ASV_Out_of_tournament=0
)

MAX_GAME_NUMBER = 1000000

def main():
    data = pd.read_csv('data.csv')
    team_symbols = data["Team_Symbol"].unique()
    # print(data.head())
    
    # Lookup table for all possible match outcome probabilities
    # 630 unique sorted pairs ((36x35)/2)
    outcome_dist_lookupTable = oc.get_match_outcome_probs(data)
    average_goals_lookupTable = dict(zip(data["Team_Symbol"], data["Average_Goals_Per_Match"]))
    
    
    for GAME_IDX in range(1, MAX_GAME_NUMBER + 1):
        if GAME_IDX % 10000 == 0: 
            print (f"{GAME_IDX} number of sims")
        ASV_SIM_Meters["Total_Runs"] += 1
        
        # These 144 random pairings are unique sets with the following constraints : 
        # 1) Each team plays exactly 8 matches
        # 2) Each team plays 2 teams from each of the 4 pots
        pairings = tm.generate_random_pairings_with_pots_df(df=data)
        # print (pairings)
        
        # simulate outcomes of all match pairings and assign pts and rank the teams
        points_and_rankings = mrk.assign_points_and_get_rankings(
                                    pairings,
                                    outcome_dist_lookupTable,
                                    team_symbols)
        
        
        
        # print("Team Rankings:")
        # for team, points in points_and_rankings.items():
        #     print(f"{team}: {points} points")
        
        ASV_Rank, teams_9_to_24 = rkh.get_rankings_help(points_and_rankings, "ASV")
        
        if ASV_Rank <= 8: 
            ASV_SIM_Meters["ASV_Qualified"] += 1
            ASV_SIM_Meters["ASV_Top_8"] += 1
            # print("ASV Rank: ", ASV_Rank)
            # print (teams_9_to_24)
            continue
        
        elif ASV_Rank >= 9 and ASV_Rank <= 24:
            ASV_SIM_Meters["ASV_Top_16_to_24_enters_2_legged"] += 1
            # print("ASV Rank: ", ASV_Rank)
            # print (teams_9_to_24)
            two_legged_outcome = ll.two_legged_sim(
                                        "ASV", 
                                        teams_9_to_24, 
                                        average_goals_lookupTable,
                                        outcome_dist_lookupTable)
            # print(two_legged_outcome)
            # print("")
            
            if two_legged_outcome == True:
                ASV_SIM_Meters["ASV_Won_2_legged"] += 1
                ASV_SIM_Meters["ASV_Qualified"] += 1
            else:
                ASV_SIM_Meters["ASV_Lost_2_legged"] += 1
                ASV_SIM_Meters["ASV_Out_of_tournament"] += 1
                
            continue
            
        elif ASV_Rank >= 25: 
            ASV_SIM_Meters["ASV_25_and_below"] += 1
            ASV_SIM_Meters["ASV_Out_of_tournament"] += 1
            # print("ASV Rank: ", ASV_Rank)
            # print (teams_9_to_24)
            continue
        
    # Print the Meters
    for key, value in ASV_SIM_Meters.items():
        print(f"{key}: {value}")
        
    prob = ASV_SIM_Meters["ASV_Qualified"]/ASV_SIM_Meters["Total_Runs"]
    print(f"Prob of ASV to qaulify : {prob}")
        

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.6f} seconds")


