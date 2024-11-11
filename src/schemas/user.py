from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: Annotated[str, Field(min_length=3, max_length=50)]
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8)]
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "secretpassword"
            }
        }

# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[Annotated[str, Field(min_length=3, max_length=50)]] = None
    full_name: Optional[str] = None
    password: Optional[Annotated[str, Field(min_length=8)]] = None
    is_active: Optional[bool] = None

# Properties to return via API
class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

# Properties for token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Properties for token data
class TokenPayload(BaseModel):
    sub: int  # user_id
    exp: datetime