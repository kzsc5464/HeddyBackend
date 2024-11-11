# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List

# from api import deps
# from schemas.profile import ProfileCreate, ProfileUpdate, Profile
# from crud.profile import profile_crud

# router = APIRouter()

# @router.get("/{username}", response_model=Profile)
# async def get_profile(
#     username: str,
#     db: AsyncSession = Depends(deps.get_db)
# ):
#     """Get user profile by username"""
#     profile = await profile_crud.get_by_username(db, username=username)
#     if not profile:
#         raise HTTPException(status_code=404, detail="Profile not found")
#     return profile

# @router.put("/me", response_model=Profile)
# async def update_profile(
#     profile_in: ProfileUpdate,
#     db: AsyncSession = Depends(deps.get_db),
#     current_user = Depends(deps.get_current_active_user)
# ):
#     """Update current user's profile"""
#     profile = await profile_crud.update(
#         db, 
#         db_obj=current_user.profile, 
#         obj_in=profile_in
#     )
#     return profile