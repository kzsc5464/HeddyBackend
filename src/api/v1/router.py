from fastapi import APIRouter
from api.v1.endpoints import user
from api.v1.endpoints import auth

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
# api_router.include_router(
#     profiles.router,
#     prefix="/profiles",
#     tags=["Profiles"]
# )

# # Item routes
# api_router.include_router(
#     items.router,
#     prefix="/items",
#     tags=["Items"]
# )

# # Search routes
# api_router.include_router(
#     search.router,
#     prefix="/search",
#     tags=["Search"]
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