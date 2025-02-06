from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from models.pet import PetType, PyObjectId

# Base Pet Schema
class PetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="반려동물의 이름")
    gender: str = Field(..., min_length=1, max_length=10, description="반려동물의 성별")
    pet_type: PetType = Field(..., description="반려동물의 종류 (DOG, CAT, OTHER)")
    breed: Optional[str] = Field(None, description="반려동물의 품종")
    weight: Optional[float] = Field(None, ge=0, description="반려동물의 체중 (kg)")
    body_type: Optional[str] = Field(None, description="반려동물의 체형")
    birth_date: Optional[datetime] = Field(None, description="반려동물의 생년월일")
    email: str = Field(..., description="반려동물 주인 아이디")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "멍멍이",
                "gender": "수컷",
                "pet_type": "DOG",
                "breed": "골든리트리버",
                "weight": 25.5,
                "body_type": "대형",
                "birth_date": "2023-01-01T00:00:00",
                "email": "<EMAIL>",
            }
        }
    )

# Create Pet Request Schema
class PetCreate(PetBase):
    pass

# Update Pet Request Schema
class PetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    gender: Optional[str] = Field(None, min_length=1, max_length=10)
    pet_type: Optional[PetType] = None
    breed: Optional[str] = None
    weight: Optional[float] = Field(None, ge=0)
    body_type: Optional[str] = None
    birth_date: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "멍멍이",
                "weight": 26.5,
                "body_type": "대형"
            }
        }
    )

# Response Schema
class PetResponse(PetBase):
    id: PyObjectId = Field(..., alias="_id")
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        json_encoders={PyObjectId: str},
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

# List Response Schema
class PetList(BaseModel):
    total: int = Field(..., description="전체 반려동물 수")
    pets: list[PetResponse] = Field(..., description="반려동물 목록")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 1,
                "pets": [{
                    "_id": "507f1f77bcf86cd799439011",
                    "name": "멍멍이",
                    "gender": "수컷",
                    "pet_type": "DOG",
                    "breed": "골든리트리버",
                    "weight": 25.5,
                    "body_type": "대형",
                    "birth_date": "2023-01-01T00:00:00",
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": None
                }]
            }
        }
    )

# Query Parameters Schema
class PetQueryParams(BaseModel):
    skip: int = Field(default=0, ge=0, description="건너뛸 데이터 수")
    limit: int = Field(default=10, ge=1, le=100, description="가져올 데이터 수")
    search: Optional[str] = Field(None, description="검색어 (이름, 품종)")
    pet_type: Optional[PetType] = Field(None, description="반려동물 종류로 필터링")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "skip": 0,
                "limit": 10,
                "search": "골든",
                "pet_type": "DOG"
            }
        }
    )

# Response Messages Schema
class ResponseMessage(BaseModel):
    status: str = Field(..., description="응답 상태")
    message: str = Field(..., description="응답 메시지")
    data: Optional[dict] = Field(None, description="추가 데이터")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "message": "반려동물이 성공적으로 등록되었습니다.",
                "data": {"pet_id": "507f1f77bcf86cd799439011"}
            }
        }
    )