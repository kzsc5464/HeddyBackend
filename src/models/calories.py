from datetime import datetime
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

class PetcaloriesCollection:
    name = "pet_health_records"

    @classmethod
    async def init_indexes(cls, db):
        collection = await db[cls.name]
        for index in cls.indexes:
            await collection.create_index(index)


    @classmethod
    async def get_pet_calories_daily_history(
            cls,
            db,
            pet_id: str,
            start_date: datetime,
            end_date: datetime,
    ) -> dict:
        collection = db[cls.name]

        pipeline = [
            {
                "$match": {
                    "pet_id": pet_id,
                    "recorded_at": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$sort": {"calories": -1}
            },
            {
                "$group": {
                    "_id": None,
                    "avg_calories": {"$avg": "$calories"},
                    "max_calories": {"$max": "$calories"},
                    "max_calories_time": {
                        "$first": {
                            "$dateToString": {
                                "format": "%H:%M",
                                "date": "$recorded_at"
                            }
                        }
                    },
                    "min_calories": {"$min": "$calories"},
                    "min_calories_time": {
                        "$last": {
                            "$dateToString": {
                                "format": "%H:%M",
                                "date": "$recorded_at"
                            }
                        }
                    }
                }
            }
        ]

        results = await collection.aggregate(pipeline).to_list(length=1)
        if not results:
            return None
        return results[0]

    @classmethod
    async def get_pet_calories_weekly_history(
            cls,
            db,
            pet_id: str,
            start_date: datetime,
            end_date: datetime
    ) -> dict:
        collection = db[cls.name]

        pipeline = [
            {
                "$match": {
                    "pet_id": pet_id,
                    "recorded_at": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$sort": {"calories": -1}
            },
            {
                "$group": {
                    "_id": None,
                    "avg_calories": {"$avg": "$calories"},
                    "max_calories": {"$max": "$calories"},
                    "max_calories_time": {
                        "$first": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$recorded_at"
                            }
                        }
                    },
                    "min_calories": {"$min": "$calories"},
                    "min_calories_time": {
                        "$last": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$recorded_at"
                            }
                        }
                    }
                }
            }
        ]

        results = await collection.aggregate(pipeline).to_list(length=1)
        if not results:
            return None
        return results[0]

    @classmethod
    async def get_pet_calories_monthly_history(
            cls,
            db,
            pet_id: str,
            start_date: datetime,
            end_date: datetime
    ) -> dict:
        collection = db[cls.name]

        pipeline = [
            {
                "$match": {
                    "pet_id": pet_id,
                    "recorded_at": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$sort": {"calories": -1}
            },
            {
                "$group": {
                    "_id": None,
                    "avg_calories": {"$avg": "$calories"},
                    "max_calories": {"$max": "$calories"},
                    "max_calories_time": {
                        "$first": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$recorded_at"
                            }
                        }
                    },
                    "min_calories": {"$min": "$calories"},
                    "min_calories_time": {
                        "$last": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$recorded_at"
                            }
                        }
                    }
                }
            }
        ]

        results = await collection.aggregate(pipeline).to_list(length=1)
        if not results:
            return None
        return results[0]

    @classmethod
    async def get_pet_calories_yearly_history(
            cls,
            db,
            pet_id: str,
            start_date: datetime,
            end_date: datetime
    ) -> dict:
        collection = db[cls.name]

        pipeline = [
            {
                "$match": {
                    "pet_id": pet_id,
                    "recorded_at": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$sort": {"calories": -1}
            },
            {
                "$group": {
                    "_id": None,
                    "avg_calories": {"$avg": "$calories"},
                    "max_calories": {"$max": "$calories"},
                    "max_calories_time": {
                        "$first": {
                            "$dateToString": {
                                "format": "%m월",
                                "date": "$recorded_at"
                            }
                        }
                    },
                    "min_calories": {"$min": "$calories"},
                    "min_calories_time": {
                        "$last": {
                            "$dateToString": {
                                "format": "%m월",
                                "date": "$recorded_at"
                            }
                        }
                    }
                }
            }
        ]

        results = await collection.aggregate(pipeline).to_list(length=1)
        if not results:
            return None
        return results[0]