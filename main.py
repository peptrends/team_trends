from fastapi import FastAPI
from trends.analytics_engine import run_analytics  # adjust import to your actual module

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/team-trends")
def team_trends():
    return run_analytics()