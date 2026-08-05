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
    # Startup: create tables (in production use Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(

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
