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

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str = Field(..., index=True)
    username: str = Field(..., min_length=3, max_length=50, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    model_config = {
        "json_encoders": {
            ObjectId: str
        },
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False
            }
        }
    }

class UserCollection:
    name = "users"
    indexes = [
        [("email", 1)],  # Unique index on email
        [("username", 1)],  # Unique index on username
        [("created_at", -1)]  # Index on created_at descending
    ]
    unique_indexes = ["email", "username"]

    @classmethod
    async def init_indexes(cls, db):
        """Initialize indexes for the collection"""
        collection = db[cls.name]
        for index in cls.indexes:
            key = index[0][0]
            is_unique = key in cls.unique_indexes
            await collection.create_index(index, unique=is_unique)

    @classmethod
    async def get_by_email(cls, db, email: str) -> Optional[User]:
        """Get user by email"""
        collection = db[cls.name]
        user_dict = await collection.find_one({"email": email})
        if user_dict:
            return User(**user_dict)
        return None

    @classmethod
    async def get_by_username(cls, db, username: str) -> Optional[User]:
        """Get user by username"""
        collection = db[cls.name]
        user_dict = await collection.find_one({"username": username})
        if user_dict:
            return User(**user_dict)
        return None

    @classmethod
    async def get_by_id(cls, db, id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            collection = db[cls.name]
            user_dict = await collection.find_one({"_id": ObjectId(id)})
            if user_dict:
                return User(**user_dict)
        except:
            return None
        return None

    @classmethod
    async def create(cls, db, user_data: dict) -> User:
        """Create new user"""
        collection = db[cls.name]
        user_data["created_at"] = datetime.utcnow()
        result = await collection.insert_one(user_data)
        user_dict = await collection.find_one({"_id": result.inserted_id})
        return User(**user_dict)

    @classmethod
    async def update(cls, db, id: str, update_data: dict) -> Optional[User]:
        """Update user"""
        collection = db[cls.name]
        update_data["updated_at"] = datetime.utcnow()
        try:
            await collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )
            return await cls.get_by_id(db, id)
        except:
            return None

    @classmethod
    async def delete(cls, db, id: str) -> bool:
        """Delete user"""
        collection = db[cls.name]
        try:
            result = await collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except:
            return False

    @classmethod
    async def update_last_login(cls, db, id: str) -> Optional[User]:
        """Update user's last login time"""
        return await cls.update(db, id, {"last_login": datetime.utcnow()})

    @classmethod
    async def list_users(
        cls,
        db,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> list[User]:
        """List users with optional search"""
        collection = db[cls.name]
        query = {}
        if search:
            query = {
                "$or": [
                    {"email": {"$regex": search, "$options": "i"}},
                    {"username": {"$regex": search, "$options": "i"}},
                    {"full_name": {"$regex": search, "$options": "i"}}
                ]
            }
        
        cursor = collection.find(query).skip(skip).limit(limit)
        users = []
        async for user_dict in cursor:
            users.append(User(**user_dict))
        return users