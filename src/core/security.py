from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from models.user import UserCollection
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.database import get_database
import time
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = await UserCollection.get_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user

def verify_auth_code(auth_code: str) -> bool:
    code = True
    if code:
        return True
    return False

def generate_password_reset_token(user_id):
    """
    사용자 ID를 토대로 비밀번호 초기화 토큰을 생성합니다.
    """
    # 토큰 생성 로직 구현
    reset_token = f"{user_id}.{int(time.time())}.{os.urandom(16).hex()}"
    return reset_token

def verify_password_reset_token(token):
    """
    비밀번호 초기화 토큰의 유효성을 확인합니다.
    """
    # 토큰 검증 로직 구현
    # ...
    return user_id

def send_password_reset_email(email, reset_token):
    """
    사용자에게 비밀번호 초기화 이메일을 전송합니다.
    """
    # 이메일 전송 로직 구현
    msg = MIMEText(f"비밀번호 초기화 링크: http://example.com/reset-password/{reset_token}")
    msg['Subject'] = "Password Reset Request"
    msg['From'] = "noreply@example.com"
    msg['To'] = email

    with smtplib.SMTP('localhost') as smtp:
        smtp.send_message(msg)