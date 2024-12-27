from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic.json_schema import GetJsonSchemaHandler
from bson import ObjectId

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
        core_schema: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string", "description": "MongoDB ObjectId"}

class PetHealth(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    pet_id: PyObjectId
    heart_rate: int = Field(..., ge=0, le=300)  # 심박수
    steps: int = Field(..., ge=0)  # 걸음 수
    calories: float = Field(..., ge=0)  # 소모 칼로리
    distance: float = Field(..., ge=0)  # 이동 거리(km)
    recorded_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }

class PetHealthCollection:
    name = "pet_health_records"
    indexes = [
        [("pet_id", 1)],
        [("recorded_at", -1)],
        [("pet_id", 1), ("recorded_at", -1)]  # 복합 인덱스
    ]

    @classmethod
    async def init_indexes(cls, db):
        collection = db[cls.name]
        for index in cls.indexes:
            await collection.create_index(index)

    @classmethod
    async def create_record(cls, db, health_data: dict) -> PetHealth:
        collection = db[cls.name]
        result = await collection.insert_one(health_data)
        record = await collection.find_one({"_id": result.inserted_id})
        return PetHealth(**record)

    @classmethod
    async def get_pet_health_history(
        cls,
        db,
        pet_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[PetHealth]:
        collection = db[cls.name]
        query = {"pet_id": ObjectId(pet_id)}
        
        if start_date or end_date:
            query["recorded_at"] = {}
            if start_date:
                query["recorded_at"]["$gte"] = start_date
            if end_date:
                query["recorded_at"]["$lte"] = end_date

        cursor = collection.find(query).sort("recorded_at", -1).limit(limit)
        records = []
        async for record in cursor:
            records.append(PetHealth(**record))
        return records

    @classmethod
    async def get_daily_summary(cls, db, pet_id: str, date: datetime) -> dict:
        collection = db[cls.name]
        start_date = datetime(date.year, date.month, date.day)
        end_date = datetime(date.year, date.month, date.day, 23, 59, 59)

        pipeline = [
            {
                "$match": {
                    "pet_id": ObjectId(pet_id),
                    "recorded_at": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "avg_heart_rate": {"$avg": "$heart_rate"},
                    "total_steps": {"$sum": "$steps"},
                    "total_calories": {"$sum": "$calories"},
                    "total_distance": {"$sum": "$distance"},
                    "records_count": {"$sum": 1}
                }
            }
        ]

        results = await collection.aggregate(pipeline).to_list(length=1)
        if not results:
            return None
        return results[0]