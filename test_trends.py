# test_trends.py

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.analytics.team_trends import (
    last_n_average,
    last_10_average,
    season_average,
    home_away_splits,
    average_margin
)

team_id = 2  # Boston Celtics

print("Boston – Last 5 average:", last_n_average(team_id, 5))
print("Boston – Last 10 average:", last_10_average(team_id))
print("Boston – Season average:", season_average(team_id))
print("Boston – Home/Away splits:", home_away_splits(team_id))
print("Boston – Average margin:", average_margin(team_id))