from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel


class PetRecordCollection:
    collection_name = "pet_records"

    @classmethod
    async def create(cls, db: AsyncIOMotorDatabase, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        새로운 반려동물 기록 생성
        """
        collection = db[cls.collection_name]
        result = await collection.insert_one(record_data)
        created_record = await collection.find_one({"_id": result.inserted_id})

        if created_record:
            created_record["_id"] = str(created_record["_id"])
        return created_record

    @classmethod
    async def get_by_id(cls, db: AsyncIOMotorDatabase, record_id: str) -> Optional[Dict[str, Any]]:
        """
        ID로 특정 기록 조회
        """
        collection = db[cls.collection_name]
        record = await collection.find_one({"_id": ObjectId(record_id)})

        if record:
            record["_id"] = str(record["_id"])
        return record

    @classmethod
    async def get_multi(
            cls,
            db: AsyncIOMotorDatabase,
            query: Dict[str, Any] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        여러 기록 조회 (페이지네이션 지원)
        """
        collection = db[cls.collection_name]
        cursor = collection.find(query or {})
        cursor = cursor.skip(skip).limit(limit)

        records = []
        async for record in cursor:
            record["_id"] = str(record["_id"])
            records.append(record)
        return records

    @classmethod
    async def update(
            cls,
            db: AsyncIOMotorDatabase,
            record_id: str,
            update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        기록 업데이트
        """
        collection = db[cls.collection_name]
        result = await collection.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": update_data}
        )

        if result.modified_count:
            updated_record = await collection.find_one({"_id": ObjectId(record_id)})
            if updated_record:
                updated_record["_id"] = str(updated_record["_id"])
            return updated_record
        return None

    @classmethod
    async def delete(cls, db: AsyncIOMotorDatabase, record_id: str) -> bool:
        """
        기록 삭제
        """
        collection = db[cls.collection_name]
        result = await collection.delete_one({"_id": ObjectId(record_id)})
        return result.deleted_count > 0

    @classmethod
    async def get_by_user_id(
            cls,
            db: AsyncIOMotorDatabase,
            user_id: str,
            skip: int = 0,
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        특정 사용자의 모든 기록 조회
        """
        return await cls.get_multi(
            db,
            query={"user_id": user_id},
            skip=skip,
            limit=limit
        )

    @classmethod
    async def count_by_user(cls, db: AsyncIOMotorDatabase, user_id: str) -> int:
        """
        사용자별 기록 수 카운트
        """
        collection = db[cls.collection_name]
        return await collection.count_documents({"user_id": user_id})

    @classmethod
    async def get_by_pet_name(
            cls,
            db: AsyncIOMotorDatabase,
            pet_name: str,
            user_id: str,
            skip: int = 0,
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        특정 반려동물 이름으로 기록 조회
        """
        return await cls.get_multi(
            db,
            query={"pet_name": pet_name, "user_id": user_id},
            skip=skip,
            limit=limit
        )

    @classmethod
    async def get_by_date_range(
            cls,
            db: AsyncIOMotorDatabase,
            user_id: str,
            start_date: datetime,
            end_date: datetime,
            skip: int = 0,
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        날짜 범위로 기록 조회
        """
        return await cls.get_multi(
            db,
            query={
                "user_id": user_id,
                "record_date": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            },
            skip=skip,
            limit=limit
        )