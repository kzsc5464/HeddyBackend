from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from core.config import settings

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect_to_database(cls):
        """Create database connection."""
        try:
            cls.client = AsyncIOMotorClient(
                settings.DATABASE_URL,
                maxPoolSize=10,
                minPoolSize=1,
            )
            cls.db = cls.client[settings.MONGO_DB]
            print("Successfully connected to MongoDB.")
            
            # 데이터베이스 연결 테스트
            await cls.db.command('ping')
            print("Pinged your deployment. Connection successful!")
            
        except Exception as e:
            print(f"Could not connect to MongoDB: {e}")
            raise e

    @classmethod
    async def close_database_connection(cls):
        """Close database connection."""
        if cls.client is not None:
            cls.client.close()
            print("MongoDB connection closed.")

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Get database instance."""
        return cls.db

async def get_database() -> AsyncIOMotorDatabase:
    """Database dependency."""
    return MongoDB.get_db()