from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routes import incoming
from src.routes import plaid
from fastapi.middleware.cors import CORSMiddleware
from src.database.client import initialize_database

ALLOWED_ORIGINS = ["http://localhost:5173", "https://vandyhacks-xi.onrender.com", "https://moneywise.wiki"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield

def initialize_application() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.include_router(incoming.router)
    app.include_router(plaid.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app