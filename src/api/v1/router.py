from fastapi import APIRouter
from api.v1.endpoints import user
from api.v1.endpoints import auth
from api.v1.endpoints import pet
from api.v1.endpoints import pethealth
from api.v1.endpoints import heart_rate
from api.v1.endpoints import calories
from api.v1.endpoints import distance
from api.v1.endpoints import steps

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

api_router.include_router(
    pethealth.router,
    prefix="/pethealth",
    tags=["pethealth"]
)

api_router.include_router(
    heart_rate.router,
    prefix="/heart_rate",
    tags=["heart_rate"]
)

api_router.include_router(
    calories.router,
    prefix="/calories",
    tags=["calories"]
)

api_router.include_router(
    distance.router,
    prefix="/distance",
    tags=["distance"]
)

# api_router.include_router(
#     steps.router,
#     prefix="/steps",
#     tags=["steps"]
# )

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