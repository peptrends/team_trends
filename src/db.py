# src/db.py

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_team_games(team_id: int):
    """
    Fetch all games for a given team_id from the 'games' table.
    """
    response = (
        supabase.table("games")
        .select("*")
        .or_(f"home_team_id.eq.{team_id},away_team_id.eq.{team_id}")
        .execute()
    )
    return response.data


def get_game_by_id(game_id: int):
    """
    Fetch a single game by its game_id.
    """
    response = (
        supabase.table("games")
        .select("*")
        .eq("game_id", game_id)
        .single()
        .execute()
    )
    return response.data


def insert_games(games: list[dict]):
    """
    Insert multiple game records into the 'games' table.
    """
    if not games:
        return None

    response = supabase.table("games").insert(games).execute()
    return response.data