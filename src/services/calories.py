from datetime import datetime

async def get_daily_heart_rate(
        cls,
        db,
        pet_id: str,
        startdate: datetime,
        enddate: datetime
) -> dict:
    collection = db[cls.name]
    start_date = datetime(startdate.year, startdate.month, startdate.day)
    end_date = datetime(enddate.year, enddate.month, enddate.day, 23, 59, 59)

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
            "$sort": {"heart_rate": -1}  # 심박수 내림차순
        },
        {
            "$group": {
                "_id": None,
                "avg_heart_rate": {"$avg": "$heart_rate"},
                "max_heart_rate": {"$max": "$heart_rate"},
                "max_heart_rate_time": {"$first": "$recorded_at"},
                "min_heart_rate": {"$min": "$heart_rate"},
                "min_heart_rate_time": {"$last": "$recorded_at"},
                "total_distance": {"$sum": "$distance"},
            }
        }
    ]

    results = await collection.aggregate(pipeline).to_list(length=1)

    print(results)

    if not results:
        return None
    return results[0]