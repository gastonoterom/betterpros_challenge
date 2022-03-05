"""Coding challenge for BetterPros"""

from fastapi import FastAPI
from src.database.models import create_tables
from src.routes.users import router as users_router
from src.routes.conversations import router as conversations_router

# FastAPI init
app = FastAPI(title="LetsChat p2p and group messaging! (patent pending)")
app.include_router(users_router)
app.include_router(conversations_router)

# Testing purposes: create the in memory tables
create_tables()
