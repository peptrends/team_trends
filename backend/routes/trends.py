from fastapi import APIRouter
from src.trends.team_trends import (
    last_n_average,
    last_10_average,
    season_average,
    home_away_splits,
    average_margins,
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

router = APIRouter()

@router.get("/team/{team_id}")
def team_trends(team_id: int):
    return {
        "offense": {
            "last_5": last_n_average(team_id, 5),
            "last_10": last_10_average(team_id),
            "season": season_average(team_id),
        },
        "defense": {
            "opp_last_5": opponent_last_5_average(team_id),
            "opp_last_10": opponent_last_10_average(team_id),
            "opp_season": opponent_season_average(team_id),
        },
        "net": {
            "net_last_5": net_last_5(team_id),
            "net_last_10": net_last_10(team_id),
            "net_season": net_season_average(team_id),
        },
        "splits": home_away_splits(team_id),
        "margins": average_margins(team_id),
        "streaks": win_loss_streak(team_id),
        "biggest": biggest_win_loss(team_id),
        "game_types": {
            "close_5": close_games(team_id, 5),
            "close_3": close_games(team_id, 3),
            "blowouts_15": blowouts(team_id, 15),
            "blowouts_20": blowouts(team_id, 20),
        }
    }

@router.get("/matchup/{home_id}/{away_id}")
def matchup_trends(home_id: int, away_id: int):
    return {
        "home": team_trends(home_id),
        "away": team_trends(away_id)
    }