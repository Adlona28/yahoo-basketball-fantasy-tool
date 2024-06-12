import unittest
import pandas as pd
from itertools import combinations

# Import the class to be tested
from leagueData import LeagueData

STATS = ['FG%', 'FT%', '3PTM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO']

class TestLeagueData(unittest.TestCase):
    def setUp(self):
        # Initialize a LeagueData instance
        self.league_data = LeagueData()
        # Add sample data
        test_csv_path = "test.csv"
        self.league_data.import_data(test_csv_path)

    def test_import_data(self):
        # Assert that team names and weeks are properly set
        expected_team_names = {"Team A", "Team B", "Team C", "Team D"}
        expected_weeks = {1, 2, 3, 4, 5, 6}
        self.assertEqual(self.league_data.teamNames, expected_team_names)
        self.assertEqual(self.league_data.weeks, expected_weeks)

        # Assert that statsByTeamPerWeek dictionary is properly populated
        expected_stats = {
            'Team A': {
                1: {'FG%': 0.45, 'FT%': 0.75, '3PTM': 10, 'PTS': 95, 'REB': 35, 'AST': 18, 'ST': 7, 'BLK': 5, 'TO': 12}, 
                2: {'FG%': 0.46, 'FT%': 0.76, '3PTM': 11, 'PTS': 102, 'REB': 38, 'AST': 20, 'ST': 8, 'BLK': 7, 'TO': 14}, 
                3: {'FG%': 0.47, 'FT%': 0.78, '3PTM': 12, 'PTS': 97, 'REB': 40, 'AST': 22, 'ST': 9, 'BLK': 6, 'TO': 15}, 
                4: {'FG%': 0.48, 'FT%': 0.79, '3PTM': 15, 'PTS': 110, 'REB': 42, 'AST': 25, 'ST': 12, 'BLK': 8, 'TO': 18}, 
                5: {'FG%': 0.47, 'FT%': 0.78, '3PTM': 14, 'PTS': 105, 'REB': 40, 'AST': 22, 'ST': 10, 'BLK': 7, 'TO': 17}, 
                6: {'FG%': 0.49, 'FT%': 0.8, '3PTM': 16, 'PTS': 112, 'REB': 45, 'AST': 25, 'ST': 12, 'BLK': 8, 'TO': 20}
                }, 
            'Team B': {
                1: {'FG%': 0.42, 'FT%': 0.78, '3PTM': 8, 'PTS': 90, 'REB': 38, 'AST': 20, 'ST': 8, 'BLK': 4, 'TO': 10}, 
                2: {'FG%': 0.4, 'FT%': 0.71, '3PTM': 7, 'PTS': 72, 'REB': 27, 'AST': 12, 'ST': 4, 'BLK': 3, 'TO': 10}, 
                3: {'FG%': 0.43, 'FT%': 0.73, '3PTM': 8, 'PTS': 80, 'REB': 32, 'AST': 14, 'ST': 6, 'BLK': 4, 'TO': 12}, 
                4: {'FG%': 0.43, 'FT%': 0.73, '3PTM': 12, 'PTS': 95, 'REB': 38, 'AST': 20, 'ST': 9, 'BLK': 7, 'TO': 15}, 
                5: {'FG%': 0.41, 'FT%': 0.75, '3PTM': 9, 'PTS': 85, 'REB': 32, 'AST': 15, 'ST': 5, 'BLK': 4, 'TO': 13}, 
                6: {'FG%': 0.45, 'FT%': 0.77, '3PTM': 12, 'PTS': 93, 'REB': 38, 'AST': 20, 'ST': 9, 'BLK': 7, 'TO': 18}
                },
            'Team C': {
                1: {'FG%': 0.41, 'FT%': 0.72, '3PTM': 9, 'PTS': 83, 'REB': 32, 'AST': 15, 'ST': 5, 'BLK': 4, 'TO': 11}, 
                2: {'FG%': 0.44, 'FT%': 0.73, '3PTM': 10, 'PTS': 95, 'REB': 33, 'AST': 18, 'ST': 9, 'BLK': 6, 'TO': 11}, 
                3: {'FG%': 0.45, 'FT%': 0.72, '3PTM': 10, 'PTS': 88, 'REB': 36, 'AST': 16, 'ST': 7, 'BLK': 5, 'TO': 13}, 
                4: {'FG%': 0.42, 'FT%': 0.75, '3PTM': 10, 'PTS': 92, 'REB': 36, 'AST': 18, 'ST': 8, 'BLK': 6, 'TO': 14}, 
                5: {'FG%': 0.43, 'FT%': 0.72, '3PTM': 11, 'PTS': 92, 'REB': 35, 'AST': 18, 'ST': 8, 'BLK': 6, 'TO': 15}, 
                6: {'FG%': 0.46, 'FT%': 0.74, '3PTM': 11, 'PTS': 98, 'REB': 40, 'AST': 22, 'ST': 10, 'BLK': 7, 'TO': 19}
                },  
            'Team D': {
                1: {'FG%': 0.43, 'FT%': 0.74, '3PTM': 7, 'PTS': 88, 'REB': 36, 'AST': 16, 'ST': 6, 'BLK': 5, 'TO': 13}, 
                2: {'FG%': 0.41, 'FT%': 0.75, '3PTM': 8, 'PTS': 85, 'REB': 32, 'AST': 14, 'ST': 5, 'BLK': 4, 'TO': 12}, 
                3: {'FG%': 0.42, 'FT%': 0.74, '3PTM': 9, 'PTS': 92, 'REB': 35, 'AST': 19, 'ST': 8, 'BLK': 5, 'TO': 12}, 
                4: {'FG%': 0.44, 'FT%': 0.77, '3PTM': 9, 'PTS': 100, 'REB': 40, 'AST': 22, 'ST': 10, 'BLK': 7, 'TO': 16}, 
                5: {'FG%': 0.43, 'FT%': 0.77, '3PTM': 10, 'PTS': 92, 'REB': 36, 'AST': 20, 'ST': 8, 'BLK': 6, 'TO': 17}, 
                6: {'FG%': 0.43, 'FT%': 0.74, '3PTM': 12, 'PTS': 97, 'REB': 38, 'AST': 20, 'ST': 9, 'BLK': 7, 'TO': 16}
                }
        }

        expected_head_to_head = {
            ('Team C', 'Team A'): {1: (1, 8), 2: (2, 7), 3: (1, 8), 4: (1, 8), 5: (1, 8), 6: (1, 8)}, 
            ('Team C', 'Team B'): {1: (1, 7), 2: (8, 1), 3: (7, 2), 4: (2, 7), 5: (7, 2), 6: (5, 3)}, 
            ('Team C', 'Team D'): {1: (2, 7), 2: (8, 1), 3: (3, 5), 4: (2, 7), 5: (2, 3), 6: (5, 2)}, 
            ('Team A', 'Team B'): {1: (4, 5), 2: (8, 1), 3: (8, 1), 4: (8, 1), 5: (8, 1), 6: (8, 1)}, 
            ('Team A', 'Team D'): {1: (7, 1), 2: (8, 1), 3: (8, 1), 4: (8, 1), 5: (8, 0), 6: (8, 1)}, 
            ('Team B', 'Team D'): {1: (7, 2), 2: (1, 8), 3: (1, 7), 4: (2, 6), 5: (1, 8), 6: (2, 2)}
        }

        for team in self.league_data.teamNames:
            for week in self.league_data.weeks:
                for stat in STATS:
                    self.assertAlmostEqual(self.league_data.statsByTeamPerWeek[team][week][stat], expected_stats[team][week][stat])

        for team_pair in combinations(self.league_data.teamNames, 2):
            swapped_team_pair = (team_pair[1], team_pair[0])
            for week in self.league_data.weeks:
                self.assertEqual(self.league_data.headToHeadResults[team_pair][week], expected_head_to_head[team_pair][week])

if __name__ == "__main__":
    unittest.main()