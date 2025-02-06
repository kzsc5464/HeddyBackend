from datetime import datetime
from typing import Optional, Any
from enum import Enum
from pydantic import BaseModel, Field, GetJsonSchemaHandler
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

class PetType(str, Enum):
    DOG = "DOG"
    CAT = "CAT"
    OTHER = "OTHER"

class Pet(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(..., min_length=1, max_length=50)
    gender: str = Field(..., min_length=1, max_length=10)
    pet_type: PetType
    breed: Optional[str] = None
    weight: Optional[float] = None
    body_type: Optional[str] = None
    birth_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    model_config = {
        "json_encoders": {
            ObjectId: str
        },
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "name": "멍멍이",
                "gender": "수컷",
                "pet_type": "DOG",
                "breed": "골든리트리버",
                "weight": 25.5,
                "body_type": "대형",
                "birth_date": "2023-01-01T00:00:00"
            }
        }
    }

class PetCollection:
    name = "pets"
    indexes = [
        [("name", 1)],
        [("pet_type", 1)],
        [("created_at", -1)]
    ]

    @classmethod
    async def init_indexes(cls, db):
        """Initialize indexes for the collection"""
        collection = db[cls.name]
        for index in cls.indexes:
            await collection.create_index(index)

    @classmethod
    async def get_by_id(cls, db, id: str) -> Optional[Pet]:
        """Get pet by ID"""
        try:
            collection = db[cls.name]
            pet_dict = await collection.find_one({"_id": ObjectId(id)})
            if pet_dict:
                return Pet(**pet_dict)
        except:
            return None
        return None

    @classmethod
    async def create(cls, db, pet_data: dict) -> Pet:
        """Create new pet"""
        collection = db[cls.name]
        pet_data["created_at"] = datetime.utcnow()
        result = await collection.insert_one(pet_data)
        pet_dict = await collection.find_one({"_id": result.inserted_id})
        return Pet(**pet_dict)

    @classmethod
    async def update(cls, db, id: str, update_data: dict) -> Optional[Pet]:
        """Update pet"""
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
        """Delete pet"""
        collection = db[cls.name]
        try:
            result = await collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except:
            return False

    @classmethod
    async def list_pets(
        cls,
        db,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        email: Optional[PetType] = None
    ) -> list[Pet]:
        """List pets with optional search and filter"""
        collection = db[cls.name]
        query = {}
        
        # Build query conditions
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"breed": {"$regex": search, "$options": "i"}}
            ]
        
        if email:
            query["email"] = email
        
        cursor = collection.find(query).skip(skip).limit(limit).sort("created_at", -1)
        pets = []
        async for pet_dict in cursor:
            pets.append(Pet(**pet_dict))
        return pets

    @classmethod
    async def get_by_type(cls, db, pet_type: PetType) -> list[Pet]:
        """Get pets by type"""
        collection = db[cls.name]
        cursor = collection.find({"pet_type": pet_type})
        pets = []
        async for pet_dict in cursor:
            pets.append(Pet(**pet_dict))
        return pets