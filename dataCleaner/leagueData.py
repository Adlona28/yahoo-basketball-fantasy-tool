import pandas as pd
from itertools import combinations

STATS = ['FG%', 'FT%', '3PTM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO']

class LeagueData:
    def __init__(self, numberOfWeeks):
        self.weeks = set(range(1, numberOfWeeks+1))
        self.teamNames = set()
        self.statsByTeamPerWeek = {}
        self.dataFrame = 0
        self.headToHeadResults = {}

    def _list_of_oponents(self, team_name):
        return [opponent_team for opponent_team in self.teamNames if opponent_team != team_name]

    def _importOneRealMatchup(self, row):
        team1 = row['Team 1 Name']
        team2 = row['Team 2 Name']
        week = row['Week']

        if week not in self.statsByTeamPerWeek[team1]:
            self.statsByTeamPerWeek[team1][week] = {}

        if week not in self.statsByTeamPerWeek[team2]:
            self.statsByTeamPerWeek[team2][week] = {}

        for stat in STATS:
            self.statsByTeamPerWeek[team1][week][stat] = row[f'Team 1 {stat}']
            self.statsByTeamPerWeek[team2][week][stat] = row[f'Team 2 {stat}']

    def _importAllHeadToHeadResults(self):
        for team_pair in combinations(self.teamNames, 2):
            self.headToHeadResults[team_pair] = {week: {} for week in self.weeks}

            for week in self.weeks:
            
                if week not in self.statsByTeamPerWeek[team_pair[0]] or week not in self.statsByTeamPerWeek[team_pair[1]]:
                    continue

                wonTeam1 = sum(1 for stat in STATS if stat == 'TO' and self.statsByTeamPerWeek[team_pair[0]][week][stat] < self.statsByTeamPerWeek[team_pair[1]][week][stat])
                wonTeam2 = sum(1 for stat in STATS if stat == 'TO' and self.statsByTeamPerWeek[team_pair[0]][week][stat] > self.statsByTeamPerWeek[team_pair[1]][week][stat])
                wonTeam1 += sum(1 for stat in STATS if stat != 'TO' and self.statsByTeamPerWeek[team_pair[0]][week][stat] > self.statsByTeamPerWeek[team_pair[1]][week][stat])
                wonTeam2 += sum(1 for stat in STATS if stat != 'TO' and self.statsByTeamPerWeek[team_pair[0]][week][stat] < self.statsByTeamPerWeek[team_pair[1]][week][stat])
                self.headToHeadResults[team_pair][week] = (wonTeam1, wonTeam2)
    

    def import_data(self, pathToCsv):
        self.dataFrame = pd.read_csv(pathToCsv)
        self.teamNames = set(self.dataFrame['Team 1 Name'].unique()) | set(self.dataFrame['Team 2 Name'].unique())
        self.statsByTeamPerWeek = {team: {} for team in self.teamNames}

        for _, row in self.dataFrame.iterrows():
            self._importOneRealMatchup(row)
        self._importAllHeadToHeadResults()

    def _get_average_result_for_team_in_week(self, team_name, week):
        # Skip if team has no data for the week (not in playoff)
        if week not in self.statsByTeamPerWeek[team_name]:
            return None
        
        # List to store results for the specified team in the specified week
        results = []

        # Iterate over headToHeadResults to find matchups involving the specified team in the specified week
        for team_pair, week_results in self.headToHeadResults.items():
            if week not in self.statsByTeamPerWeek[team_pair[0]] or week not in self.statsByTeamPerWeek[team_pair[1]]:
                continue
            if week in week_results and team_name in team_pair:
                # Add result for the specified team in the specified week
                results.append(week_results[week][team_pair.index(team_name)])

        # Calculate the average result
        if results:
            average_result = sum(results) / len(results)
            return average_result
        else:
            return None
        
    def get_average_stats_ranking(self, week=None):

        # If week is provided, calculate average stats for that week only
        if week is not None:
            average_results = []
            for team_name in self.teamNames:
                average_result = self._get_average_result_for_team_in_week(team_name, week)
                if average_result is not None:
                    average_results.append((team_name, average_result))
        else:
            average_results = []
            for team_name in self.teamNames:
                for week in self.weeks:
                    average_result = self._get_average_result_for_team_in_week(team_name, week)
                    if average_result is not None:
                        average_results.append((team_name, week, average_result))

        # Rank teams based on their average results
        ranked_teams = sorted(average_results, key=lambda x: x[-1], reverse=True)

        return ranked_teams

    def _get_wins_for_team_in_week(self, team_name, week):
        # Skip if team has no data for the week (not in playoff)
        if week not in self.statsByTeamPerWeek[team_name]:
            return None
        
        totalWins = 0

        for team_pair, week_results in self.headToHeadResults.items():
            if week not in self.statsByTeamPerWeek[team_pair[0]] or week not in self.statsByTeamPerWeek[team_pair[1]]:
                continue
            if week in week_results and team_name in team_pair:
                if week_results[week][team_pair.index(team_name)] > week_results[week][1-team_pair.index(team_name)]:
                    totalWins += 1

        return totalWins
        
    def get_wins_ranking(self, week):
        # Dictionary to store average results for all teams in the specified week
        wins_results = {}

        # Iterate over all teams to calculate average results for each team in the specified week
        for team_name in self.teamNames:
            wins_result = self._get_wins_for_team_in_week(team_name, week)
            if wins_result is not None:
                wins_results[team_name] = wins_result

        # Rank teams based on their average results
        ranked_teams = sorted(wins_results.items(), key=lambda x: x[1], reverse=True)

        return ranked_teams

    def print_head_to_head_results(self, team1, team2):
        
        if (team1, team2) not in self.headToHeadResults:
            aux = team1
            team1 = team2
            team2 = aux
        print(f"\n{team1} VS {team2}")
        print("-" * 20)
        winsTeam1 = 0
        winsTeam2 = 0
        ties = 0

        for week in self.weeks:
            team1_result = self.headToHeadResults[(team1, team2)][week][0]
            team2_result = self.headToHeadResults[(team1, team2)][week][1]
            print(f"Setmana {week}: {team1_result}-{team2_result}")

            if team1_result > team2_result:
                winsTeam1 += 1
            elif team1_result < team2_result:
                winsTeam2 += 1
            else:
                ties += 1
        print(f"Total:  {team1} {winsTeam1}  {team2} {winsTeam2}  {ties} empats\n")

    def get_data(self, key):
        return self.data.get(key, "No data found for this key")

# Initialize a LeagueData instance
league_data = LeagueData(23)
# Add sample data
csv_path = "Yahoo-428.l.17058-Matchup.csv"
league_data.import_data(csv_path)
week = 23
ranked_teams_by_average_stats = league_data.get_average_stats_ranking(week)

print("Ranking by average stats on week " + str(week) + ":")
for rank, (team_name, result) in enumerate(ranked_teams_by_average_stats, start=1):
    print(f"{rank}. {team_name}: {result:.2f}")

ranked_teams_by_wins = league_data.get_wins_ranking(week)

print("Ranking by wins on week " + str(week) + ":")
for rank, (team_name, result) in enumerate(ranked_teams_by_wins, start=1):
    print(f"{rank}. {team_name}: {result}")

league_data.print_head_to_head_results('PistosCF', 'Danilovic a fool')

#ranking de totes les setmanes
#ranked_teams_by_average_stats_all_weeks = league_data.get_average_stats_ranking()
#print("Ranking by average stats:")
#for rank, (team_name, week, result) in enumerate(ranked_teams_by_average_stats_all_weeks, start=1):
#    print(f"{rank}. {team_name}, setmana {week}: {result:.2f}")

#ranking mig tota la temporada
ranked_teams_by_average_stats_all_weeks = league_data.get_average_stats_ranking()
print("Ranking all season by avg stats:")
team_results = {}
# Iterate over the ranked teams by average stats for all weeks
for team_name, week, result in ranked_teams_by_average_stats_all_weeks:
    if team_name not in team_results:
        # If the team is not yet in the dictionary, initialize its entry
        team_results[team_name] = {'total_avg': 0, 'weeks': {}}
    # Update the total average result for the team
    team_results[team_name]['total_avg'] += result
    # Update the average result for the current week
    team_results[team_name]['weeks'][week] = result

sorted_team_results = sorted(team_results.items(), key=lambda x: x[1]['total_avg'], reverse=True)
# Iterate over the aggregated results and print the ranking
for rank, (team_name, team_data) in enumerate(team_results.items(), start=1):
    total_avg = team_data['total_avg'] / len(team_data['weeks'])
    print(f"{rank}. {team_name}: Total Average: {total_avg:.2f}")

def print_main_menu():
    print("\nMain Menu:")
    print("1. Import data")
    print("2. Retrieve data")
    print("3. Exit")


def print_retrieve_menu():
    print("\nRetrieve Menu:")
    print("1. Retrieve all data")
    print("2. Retrieve specific data")
    print("3. Back to main menu")


def retrieve_specific_data(data_obj):
    key = input("Enter key to retrieve data: ")
    print(data_obj.get_data(key))


def main():
    data_obj = DataObject()

    while True:
        print_main_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            key = input("Enter key: ")
            value = input("Enter value: ")
            data_obj.add_data(key, value)
            print("Data added successfully!")
        elif choice == "2":
            while True:
                print_retrieve_menu()
                retrieve_choice = input("Enter your choice: ")
                if retrieve_choice == "1":
                    # Retrieve all data
                    print("All data:")
                    for key, value in data_obj.data.items():
                        print(f"{key}: {value}")
                elif retrieve_choice == "2":
                    # Retrieve specific data
                    retrieve_specific_data(data_obj)
                elif retrieve_choice == "3":
                    break  # Go back to main menu
                else:
                    print("Invalid choice. Please choose a valid option.")
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()