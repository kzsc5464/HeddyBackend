from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import timedelta

from core.config import settings
from core.database import get_database
from core.security import verify_password, create_access_token, get_current_user
from models.user import UserCollection
from models.auth_code import AuthCollection
from schemas.user import Token
from core.security import verify_auth_code

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Try to authenticate with email
    user = await UserCollection.get_by_email(db, form_data.username)
    
    # If user not found with email, try username
    if not user:
        user = await UserCollection.get_by_username(db, form_data.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Update last login time
    await UserCollection.update_last_login(db, str(user.id))
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/password-reset")
async def request_password_reset(
        email: str,
        auth_code: int,
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    auth_code = await AuthCollection.get_by_authcode(db, email, auth_code)
    if not auth_code:
        raise HTTPException(status_code=404, detail="auth code not found")

    return {"detail": "Password reset instructions have been sent to your email."}


@router.post("/password-reset/{token}")
async def reset_password(
        token: str,
        new_password: str,
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    user_id = verify_password_reset_token(token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired password reset token.")

    user = await UserCollection.get_by_id(db, user_id)
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(new_password)
    await UserCollection.update(db, user_id, user_dict)

    return {"detail": "Password has been reset successfully."}


@router.post("/update-password")
async def update_password(
        user_id: str,
        auth_code: str,
        new_password: str,
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    # 인증 코드 확인
    if not verify_auth_code(user_id, auth_code):
        raise HTTPException(status_code=400, detail="Invalid authentication code")

    # 비밀번호 변경
    user = await UserCollection.get_by_id(db, ObjectId(user_id))
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(new_password)
    await UserCollection.update(db, user_id, user_dict)

    return {"detail": "Password updated successfully"}

@router.post("/test-token", response_model=None)
async def test_token(current_user = Depends(get_current_user)):
    """
    Test access token
    """
    return {
        "email": current_user.email,
        "username": current_user.username
    }