# src/trends/loaders.py
from .db import supabase

def get_team_games(team_id: int):
    response = (
        supabase.table("games")
        .select("*")
        .or_(f"home_team_id.eq.{team_id},away_team_id.eq.{team_id}")
        .order("date", desc=False)
        .execute()
    )
    return response.data or []