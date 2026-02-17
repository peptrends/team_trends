# test_trends_full.py

from src.trends.team_trends import (
    # Phase 1 / early metrics
    last_n_average,
    last_10_average,
    season_average,
    home_away_splits,
    average_margins,

    # Phase 2 metrics
    win_loss_streak,
    biggest_win_loss,
    close_games,
    blowouts,
    opponent_last_5_average,
    opponent_last_10_average,
    opponent_season_average,
    net_last_5,
    net_last_10,
    net_season_average
)

team_id = 2  # Boston Celtics

print("\n=== OFFENSIVE TRENDS ===")
print("Last 5 average:", last_n_average(team_id, 5))
print("Last 10 average:", last_10_average(team_id))
print("Season average:", season_average(team_id))

print("\n=== CONTEXTUAL SPLITS ===")
print("Home/Away splits:", home_away_splits(team_id))

print("\n=== MARGIN TRENDS ===")
print("Average margins:", average_margins(team_id))
print("Biggest win/loss:", biggest_win_loss(team_id))

print("\n=== GAME TYPE COUNTS ===")
print("Close games (<=5):", close_games(team_id, threshold=5))
print("Close games (<=3):", close_games(team_id, threshold=3))
print("Blowouts (>=15):", blowouts(team_id, threshold=15))
print("Blowouts (>=20):", blowouts(team_id, threshold=20))

print("\n=== STREAKS ===")
print("Win/Loss streak:", win_loss_streak(team_id))

print("\n=== DEFENSIVE TRENDS ===")
print("Opponent last 5 avg:", opponent_last_5_average(team_id))
print("Opponent last 10 avg:", opponent_last_10_average(team_id))
print("Opponent season avg:", opponent_season_average(team_id))

print("\n=== NET SCORING TRENDS ===")
print("Net last 5:", net_last_5(team_id))
print("Net last 10:", net_last_10(team_id))
print("Net season average:", net_season_average(team_id))

print("\n=== DONE ===\n")