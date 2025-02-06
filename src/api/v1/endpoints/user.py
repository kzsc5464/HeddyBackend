# API endpoint에서 사용 예시
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.database import get_database
from models.user import UserCollection
from schemas.user import UserCreate
from core.security import get_password_hash
router = APIRouter()

@router.post("/")
async def create_user(
    user_data: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # 이메일 중복 체크
    existing_user = await UserCollection.get_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 사용자 생성
    user_dict = user_data.dict()
    user_dict["hashed_password"] = get_password_hash(user_data.password)
    user = await UserCollection.create(db, user_dict)
    return {"status": "success"}

@router.get("/{user_id}")
async def get_user(
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    user = await UserCollection.get_by_username(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user