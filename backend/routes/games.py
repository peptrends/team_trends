from fastapi import APIRouter
from datetime import date
from supabase import create_client
import os

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.get("/today")
def get_todays_games():
    today = date.today().isoformat()

    response = (
        supabase.table("games")
        .select("id, home_team_name, away_team_name, date, status")
        .eq("date", today)
        .execute()
    )

    return response.data