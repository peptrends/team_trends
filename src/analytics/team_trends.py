from src.db import get_team_games
from src.calculations import safe_div


# ------------------------------------------------------------
# Helper: extract scores from the ONLY valid columns
# ------------------------------------------------------------
def extract_scores(g):
    """
    Uses the single authoritative schema:
    home_score / away_score
    """
    return g.get("home_score"), g.get("away_score")


# ------------------------------------------------------------
# Helper: compute averages for a list of completed games
# ------------------------------------------------------------
def _compute_averages(team_id, games):
    valid_games = []

    for g in games:
        home, away = extract_scores(g)
        if home is None or away is None:
            continue
        valid_games.append(g)

    if not valid_games:
        return {
            "games": 0,
            "avg_points_for": 0,
            "avg_points_against": 0,
            "avg_margin": 0,
        }

    total_for = 0
    total_against = 0
    total_margin = 0

    for g in valid_games:
        home, away = extract_scores(g)

        if g["home_team_id"] == team_id:
            pts_for = home
            pts_against = away
        else:
            pts_for = away
            pts_against = home

        total_for += pts_for
        total_against += pts_against
        total_margin += (pts_for - pts_against)

    games_count = len(valid_games)

    return {
        "games": games_count,
        "avg_points_for": safe_div(total_for, games_count),
        "avg_points_against": safe_div(total_against, games_count),
        "avg_margin": safe_div(total_margin, games_count),
    }


# ------------------------------------------------------------
# Last N games (completed only)
# ------------------------------------------------------------
def last_n_average(team_id: int, n: int):
    games = get_team_games(team_id) or []

    # Keep only completed games
    completed = []
    for g in games:
        home, away = extract_scores(g)
        if home is None or away is None:
            continue
        completed.append(g)

    if not completed:
        return {
            "games": 0,
            "avg_points_for": 0,
            "avg_points_against": 0,
            "avg_margin": 0,
        }

    # Sort by date
    completed.sort(key=lambda g: g["date"])

    # Take last N completed games
    recent = completed[-n:]

    return _compute_averages(team_id, recent)


def last_5_average(team_id: int):
    return last_n_average(team_id, 5)


def last_10_average(team_id: int):
    return last_n_average(team_id, 10)


# ------------------------------------------------------------
# Season average (completed games only)
# ------------------------------------------------------------
def season_average(team_id: int):
    games = get_team_games(team_id) or []
    return _compute_averages(team_id, games)


# ------------------------------------------------------------
# Home / Away splits
# ------------------------------------------------------------
def home_away_splits(team_id: int):
    games = get_team_games(team_id) or []

    home_games = []
    away_games = []

    for g in games:
        home, away = extract_scores(g)
        if home is None or away is None:
            continue

        if g["home_team_id"] == team_id:
            home_games.append(g)
        elif g["away_team_id"] == team_id:
            away_games.append(g)

    def avg_margin(glist):
        if not glist:
            return 0
        total = 0
        for g in glist:
            home, away = extract_scores(g)
            if g["home_team_id"] == team_id:
                total += (home - away)
            else:
                total += (away - home)
        return safe_div(total, len(glist))

    return {
        "home_games": len(home_games),
        "away_games": len(away_games),
        "home_avg_margin": avg_margin(home_games),
        "away_avg_margin": avg_margin(away_games),
    }


# ------------------------------------------------------------
# Average margins (completed games only)
# ------------------------------------------------------------
def average_margin(team_id: int):
    games = get_team_games(team_id) or []

    completed = []
    for g in games:
        home, away = extract_scores(g)
        if home is None or away is None:
            continue
        completed.append(g)

    if not completed:
        return {
            "games": 0,
            "avg_margin": 0,
        }

    def margin(g):
        home, away = extract_scores(g)
        if g["home_team_id"] == team_id:
            return home - away
        else:
            return away - home

    margins = [margin(g) for g in completed]
    avg_margin = safe_div(sum(margins), len(margins))

    return {
        "games": len(completed),
        "avg_margin": avg_margin,
    }