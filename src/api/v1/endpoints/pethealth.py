from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, date, timedelta
from typing import List, Optional
from core.database import get_database
from core.security import get_current_user
from models.pet_health import PetHealth, PetHealthCollection
from utils.set_time import convert_date_to_datetime_range, convert_date_afternonn, conver_date_night



router = APIRouter()

@router.post("/health", response_model=PetHealth)
async def record_pet_health(
    pet_id: str,
    heart_rate: int = Query(..., ge=0, le=300),
    steps: int = Query(..., ge=0),
    calories: float = Query(..., ge=0),
    distance: float = Query(..., ge=0),
    db: AsyncIOMotorDatabase = Depends(get_database)
    # current_user = Depends(get_current_user)
):
    """
    Record new health data for a pet
    """
    health_data = {
        "pet_id": ObjectId(pet_id),
        "heart_rate": heart_rate,
        "steps": steps,
        "calories": calories,
        "distance": distance,
        "recorded_at": datetime.utcnow()
    }
    
    try:
        record = await PetHealthCollection.create_record(db, health_data)
        return record
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/health/{pet_id}/history", response_model=List[PetHealth])
async def get_pet_health_history(
    pet_id: str,
    start_date,
    end_date,
    limit: int = Query(default=100, le=1000),
    db: AsyncIOMotorDatabase = Depends(get_database)
    # current_user = Depends(get_current_user)
):
    """
    Get pet's health history with optional date range filter
    """

    start_date, end_date = convert_date_to_datetime_range(start_date, end_date)

    try:
        records = await PetHealthCollection.get_pet_health_history(
            db,
            pet_id,
            start_date,
            end_date,
            limit
        )
        return records
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/health/{pet_id}/heart_rate/aggregate")
async def get_daily_heart_rate(
    pet_id: str,
    start_date,
    end_date,
    db: AsyncIOMotorDatabase = Depends(get_database)
    # current_user = Depends(get_current_user)
):
    """
    Get daily summary of pet's health metrics
    """

    start_date, end_date = convert_date_to_datetime_range(start_date, end_date)
    print(start_date)
    print(end_date)
    try:
        # if date is None:
        #     date = datetime.utcnow().date()
        
        summary = await PetHealthCollection.get_daily_heart_rate(
            db,
            pet_id,
            start_date,
            end_date
        )
        if not summary:
            raise HTTPException(status_code=404, detail="No records found for this date")
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health/{pet_id}/heart_rate/aggregate")
async def get_daily_heart_rate(
        pet_id: str,
        start_date,
        end_date,
        db: AsyncIOMotorDatabase = Depends(get_database)
        # current_user = Depends(get_current_user)
):
    """
    Get daily summary of pet's health metrics
    """

    start_date, end_date = convert_date_to_datetime_range(start_date, end_date)
    print(start_date)
    print(end_date)
    try:
        # if date is None:
        #     date = datetime.utcnow().date()

        summary = await PetHealthCollection.get_daily_heart_rate(
            db,
            pet_id,
            start_date,
            end_date
        )
        if not summary:
            raise HTTPException(status_code=404, detail="No records found for this date")
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))