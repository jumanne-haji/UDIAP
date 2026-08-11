"""
UDIAP – Universal Decision Intelligence Assessment Platform
FastAPI Backend Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import engine, Base
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database schema is managed exclusively by Alembic.
    yield
    await engine.dispose()


app = FastAPI(

title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Universal Decision Intelligence Assessment Platform – "
        "AI-powered analysis of human decision processes via "
        "Cognitive Observer Engine (COE) and Human Decision Process Model (HDPM)."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://udiap.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "message": "Measure How Humans Think, Decide and Adapt.",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ready")
async def readiness():
    """Database readiness probe."""
    from sqlalchemy import text
    from app.core.database import AsyncSessionLocal

    try:
        async with AsyncSessionLocal() as db:
            await db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected",
        }
    except Exception:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "database": "disconnected",
            },
        )
