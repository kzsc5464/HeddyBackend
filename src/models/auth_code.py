from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, Field, GetJsonSchemaHandler
from bson import ObjectId
from pydantic.json_schema import JsonSchemaValue


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, info):
        if not isinstance(value, ObjectId):
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            value = ObjectId(value)
        return value

    @classmethod
    def __get_pydantic_json_schema__(
            cls,
            _schema_generator: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        return {
            'type': 'string',
            'description': 'MongoDB ObjectId'
        }


class auth_code(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str = Field(..., index=True)
    auth_code : int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_encoders": {
            ObjectId: str
        },
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "auth_code": "12345678",
            }
        }
    }


class AuthCollection:
    name = "auth_code"
    @classmethod
    async def init_indexes(cls, db):
        """Initialize indexes for the collection"""
        collection = db[cls.name]

        # TTL 인덱스 생성
        ttl_index = [("created_at", 1)]
        await collection.create_index(ttl_index, expireAfterSeconds=180)

    @classmethod
    async def get_by_authcode(cls, db, email: str, auth_code: int) -> Optional[auth_code]:
        """Get user by email"""
        collection = db[cls.name]
        auth_code_dict = await collection.find_one({"email": email, "auth_code": auth_code})
        if auth_code_dict:
            return True
        return False

    @classmethod
    async def create(cls, db, auth_code: dict) -> auth_code:
        """Create new user"""
        collection = db[cls.name]
        auth_code["created_at"] = datetime.utcnow()
        result = await collection.insert_one(auth_code)
        return result