import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.database import AsyncSessionLocal
from app.routers import auth, users

# Configure structured JSON logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.get_logger()

app = FastAPI(
    title="Tlanner — User Service",
    description="Handles user registration, authentication, and profiles.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — in dev we allow all origins, tighten this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_env == "development" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers under /api/v1
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint used by Docker and Kubernetes probes.

    Verifies the service is running AND the database is reachable.
    """
    db_status = "unreachable"
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            db_status = "connected"
    except Exception as e:
        logger.error("health_check_db_failed", error=str(e))

    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "service": "user-service",
        "db": db_status,
    }


@app.on_event("startup")
async def on_startup():
    logger.info("user_service_starting", env=settings.app_env)
