from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.database import get_database
from utils.set_time import conver_date_night, convert_date_afternonn, convert_date_to_datetime_range

# Schemas

router = APIRouter()

@router.get("/{pet_id}/daily")
async def get_daily_calories(
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

@router.get("/{pet_id}/monthly")
async def get_monthly_calories(
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