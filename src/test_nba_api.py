from nba_api.stats.static import teams

all_teams = teams.get_teams()
print(f"Found {len(all_teams)} teams")
print(all_teams[0])

