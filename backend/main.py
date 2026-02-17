from fastapi import FastAPI
from routes.games import router as games_router
from routes.trends import router as trends_router

app = FastAPI(
    title="NBA Team Trends API",
    description="Backend API for NBA analytics app",
    version="1.0"
)

app.include_router(games_router, prefix="/games", tags=["Games"])
app.include_router(trends_router, prefix="/trends", tags=["Trends"])