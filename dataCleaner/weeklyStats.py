import pandas as pd

STATS = ['Points', 'FG%', 'FT%', '3PTM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO']

def compare_team_positions(rankings, team1, team2):

    team1_count = sum(rankings[stat].index(team1) < rankings[stat].index(team2) for stat in rankings)
    team2_count = sum(rankings[stat].index(team2) < rankings[stat].index(team1) for stat in rankings)

    if team1_count > team2_count:
        return team1
    elif team2_count > team1_count:
        return team2
    else:
        return "Tie"

def get_rankings(team_data, week):

    rankings = {stat: [] for stat in STATS}

    for stat in STATS:
        team_stat_values = [(team, team_data[team][week][stat]) for team in team_data if week in team_data[team]]
        if stat == "TO":
            team_stat_values.sort(key=lambda x: x[1], reverse=False)
        else:
            team_stat_values.sort(key=lambda x: x[1], reverse=True)
        
        rankings[stat] = [team for team, stat in team_stat_values]

    return rankings

def getAllWins(rankings, team_names):
    winningSets = {team: set() for team in team_names}

    for team in team_names:
        for other_team in team_names:
            if team == other_team:
                continue

            better_team = compare_team_positions(rankings, team, other_team)
            if better_team == team:
                winningSets[team].add(other_team)

    return winningSets

def get_team_wins_summary(rankings, team_names):
    winning_sets = getAllWins(rankings, team_names)

    # Initialize a dictionary to store the total wins for each team
    total_wins = {team: 0 for team in team_names}

    for team, wins_against in winning_sets.items():
        total_wins[team] = len(wins_against)

    team_wins_summary = [(team, total_wins[team]) for team in team_names]
    team_wins_summary.sort(key=lambda x: x[1], reverse=True)

    return team_wins_summary

# Replace 'your_file.csv' with the actual path to your CSV file
file_path = 'Yahoo-428.l.17058-Matchup.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

team_names = set(df['Team 1 Name'].unique()) | set(df['Team 2 Name'].unique())
team_data = {team: {} for team in team_names}
weeks = set(df['Week'].unique())
stats_names = {'Points', 'FG%', 'FT%', '3PTM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO'}

# Iterate through rows in the DataFrame and populate the dictionary
for index, row in df.iterrows():
    team1 = row['Team 1 Name']
    team2 = row['Team 2 Name']
    week = row['Week']

    # Initialize the team's dictionary for the week if it doesn't exist
    if week not in team_data[team1]:
        team_data[team1][week] = {}
    if week not in team_data[team2]:
        team_data[team2][week] = {}

    # Populate the dictionary with stats for each team in each week
    team_data[team1][week] = {
        'Points': row['Team 1 Points'],
        'FG%': row['Team 1 FG%'],
        'FT%': row['Team 1 FT%'],
        '3PTM': row['Team 1 3PTM'],
        'PTS': row['Team 1 PTS'],
        'REB': row['Team 1 REB'],
        'AST': row['Team 1 AST'],
        'ST': row['Team 1 ST'],
        'BLK': row['Team 1 BLK'],
        'TO': row['Team 1 TO'],
    }

    team_data[team2][week] = {
        'Points': row['Team 2 Points'],
        'FG%': row['Team 2 FG%'],
        'FT%': row['Team 2 FT%'],
        '3PTM': row['Team 2 3PTM'],
        'PTS': row['Team 2 PTS'],
        'REB': row['Team 2 REB'],
        'AST': row['Team 2 AST'],
        'ST': row['Team 2 ST'],
        'BLK': row['Team 2 BLK'],
        'TO': row['Team 2 TO'],
    }

def _list_of_oponents(team_name, team_names):
    return [opponent_team for opponent_team in team_names if opponent_team != team_name]


# Print the result as a dictionary
#print(team_data)

for week in weeks:
    rankings = get_rankings(team_data, week)
    teamWinsRanking = get_team_wins_summary(rankings, team_names)
    print()
    print("Setmana " + str(week) + ":")
    for team, wins in teamWinsRanking:
        print(team + " " + str(wins))

# Initialize a dictionary to store the number of stat comparisons won by each team per week against every opponent
team_wins_per_week_against_opponents = {team: {opponent: {week: 0 for week in weeks} for opponent in team_names if opponent != team} for team in team_names}

# Iterate through weeks, teams, and opponents to compare stats
for week in weeks:
    for team in team_names:
        # Skip teams that don't have data for the current week
        if week not in team_data[team]:
            continue

        team_stats = team_data[team][week]

        # Compare stats with every possible opponent
        for opponent in _list_of_oponents(team, team_names):
            opponent_stats = team_data[opponent][week]

            # Count the number of stat comparisons won by the team against the opponent for the current week
            comparisons_won = 0

            # Add a comparison for turnovers where the team with less TO wins
            if team_stats['TO'] < opponent_stats['TO']:
                comparisons_won += 1

            # Add comparisons for other stats where the team with greater values wins
            comparisons_won += sum(1 for stat in stats_names if team_stats[stat] > opponent_stats[stat] and stat != 'TO')

            team_wins_per_week_against_opponents[team][opponent][week] = comparisons_won

# Display the number of stat comparisons won by each team against every opponent for each week
for team, opponent_wins_per_week in team_wins_per_week_against_opponents.items():
    for opponent, wins_per_week in opponent_wins_per_week.items():
        print(f"{team} vs {opponent}: {wins_per_week}")

# Initialize dictionaries to store total wins and average wins for each team against every opponent
total_wins_vs_opponent = {team: {opponent: 0 for opponent in team_names if opponent != team} for team in team_names}
total_wins_per_week = {team: {week: 0 for week in weeks} for team in team_names}

# Iterate through teams and opponents to accumulate wins
for team in team_names:
    for opponent in _list_of_oponents(team, team_names):
        total_wins_vs_opponent[team][opponent] = sum(team_wins_per_week_against_opponents[team][opponent].values())

    for week in weeks:
        total_wins_per_week[team][week] = sum(opponent_values[week] for opponent_values in team_wins_per_week_against_opponents[team].values())

#Media de victorias de toda la temporada
for team in team_names:
    total_wins = sum(total_wins_vs_opponent[team].values())
    average_wins = total_wins/(len(team_names)*len(weeks))
    print(team + " " + str(average_wins))

for week in weeks:
    weekRanking = []
    
    for team in team_names:
        total_wins = 0
        
        for opponent in _list_of_oponents(team, team_names):
            total_wins += team_wins_per_week_against_opponents[team][opponent][week]
        weekRanking.append([team, total_wins])
    weekRanking.sort(key=lambda x: x[1], reverse=True)
    print()
    print("Setmana " + str(week))
    for [team, wins] in weekRanking:
        print(team + ": " + str(wins/15.0))