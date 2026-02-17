from src.db import get_team_games

games = get_team_games(2)

print("TOTAL GAMES RETURNED:", len(games))
print()

for g in games:
    print(g["date"], g["home_team_score"], g["away_team_score"])