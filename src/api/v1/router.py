from fastapi import APIRouter
from api.v1.endpoints import user
from api.v1.endpoints import auth
from api.v1.endpoints import pet

# Main API Router
api_router = APIRouter()

# Auth routes
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# User routes
api_router.include_router(
    user.router,
    prefix="/user",
    tags=["User"]
)

# # Profile routes
api_router.include_router(
    pet.router,
    prefix="/pet",
    tags=["pet"]
)

# Email Auth
api_router.include_router(
    pet.router,
    prefix="/email",
    tags=["email"]
)

# Health check
@api_router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

# Version check
@api_router.get("/version", tags=["Version"])
async def get_version():
    return {
        "version": "1.0.0",
        "api_version": "v1"
    }