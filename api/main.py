from fastapi import FastAPI
from src.analytics.team_trends import (
    last_n_average,
    season_average,
    home_away_splits,
    average_margin
)

app = FastAPI()

@app.get("/team/{team_id}/trends")
def team_trends(team_id: int):
    return {
        "last_5": last_n_average(team_id, 5),
        "last_10": last_n_average(team_id, 10),
        "season": season_average(team_id),
        "home_away": home_away_splits(team_id),
        "average_margin": average_margin(team_id),
    }