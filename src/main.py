from fastapi import FastAPI
from core.config import settings
from api.v1.router import api_router
from core.database import MongoDB

app = FastAPI(**settings.fastapi_kwargs)

# Setup CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
async def startup_db_client():
    """Database connection on startup."""
    await MongoDB.connect_to_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    """Database disconnection on shutdown."""
    await MongoDB.close_database_connection()

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Heddy Backend API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        db = MongoDB.get_db()
        await db.command('ping')
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": str(e)
        }

