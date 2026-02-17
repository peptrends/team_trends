import os
import time
import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BASE_URL = "https://api.balldontlie.io/v1"
API_KEY = os.getenv("BALLDONTLIE_API_KEY")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def safe_int(value):
    try:
        return int(value)
    except:
        return None

def fetch_json(url, params=None):
    """Fetch JSON with retries and rate-limit handling."""
    for attempt in range(5):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=10)

            if r.status_code == 429:
                print("Rate limited. Sleeping 3 seconds...")
                time.sleep(3)
                continue

            r.raise_for_status()
            return r.json()

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            time.sleep(2)

    return None

# ---------------------------------------------------------
# TEAMS
# ---------------------------------------------------------

def fetch_teams():
    print("Fetching teams...")
    data = fetch_json(f"{BASE_URL}/teams")

    if not data or "data" not in data:
        print("Failed to fetch teams.")
        return

    teams = []
    for t in data["data"]:
        teams.append({
            "id": safe_int(t.get("id")),
            "name": t.get("name"),
            "full_name": t.get("full_name"),
            "city": t.get("city"),
            "abbreviation": t.get("abbreviation"),
        })

    print(f"Found {len(teams)} teams. Inserting...")
    supabase.table("teams").upsert(teams).execute()

# ---------------------------------------------------------
# GAMES
# ---------------------------------------------------------

def upsert_games(games):
    """Insert games safely, skipping malformed ones."""
    cleaned = []

    for g in games:

        if "home_team" not in g or g["home_team"] is None:
            print(f"Skipping malformed game (missing home_team): {g.get('id')}")
            continue

        if "visitor_team" not in g or g["visitor_team"] is None:
            print(f"Skipping malformed game (missing visitor_team): {g.get('id')}")
            continue

        cleaned.append({
            "id": safe_int(g.get("id")),
            "date": g.get("date"),
            "season": safe_int(g.get("season")),
            "home_team_id": safe_int(g["home_team"].get("id")),
            "away_team_id": safe_int(g["visitor_team"].get("id")),
            "home_score": safe_int(g.get("home_team_score")),
            "away_score": safe_int(g.get("visitor_team_score")),
        })

    if cleaned:
        supabase.table("games").upsert(cleaned).execute()

# ---------------------------------------------------------
# MAIN SEASON LOADER (CURSOR PAGINATION)
# ---------------------------------------------------------

def load_season(season):
    print(f"Loading season {season}...")

    fetch_teams()

    print("Fetching games...")

    cursor = None
    per_page = 100

    while True:
        print(f"Fetching cursor: {cursor}")

        params = {"seasons[]": season, "per_page": per_page}
        if cursor:
            params["cursor"] = cursor

        data = fetch_json(f"{BASE_URL}/games", params=params)

        # If API returns nothing (rate limit exhaustion), retry same cursor
        if not data or "data" not in data:
            print("No data returned. Likely rate limit exhaustion. Sleeping 5 seconds and retrying...")
            time.sleep(5)
            continue

        games = data["data"]
        if not games:
            print("No games returned. Stopping.")
            break

        try:
            upsert_games(games)
        except Exception as e:
            print("Error while inserting games.")
            print(e)
            print("You can re-run the script; it will resume automatically.")
            break

        meta = data.get("meta", {})
        next_cursor = meta.get("next_cursor")

        if not next_cursor:
            print("No next_cursor. Finished all pages.")
            break

        cursor = next_cursor

        # Slow down to avoid rate limits
        time.sleep(1.5)

# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

if __name__ == "__main__":
    load_season(2025)