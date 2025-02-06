from utils.set_time import convert_date_to_datetime_range
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.database import get_database
from services.calories import PetCaloriesService
# from schemas.calories import DailyCaloriesResponse

router = APIRouter()
calories_service = PetCaloriesService()

@router.get("/{pet_id}/daily")
async def get_daily_calories(
        pet_id: str,
        date: str,
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get daily summary of pet's calories"""
    try:
        summary = await calories_service.daily_calories(
            db=db,
            pet_id=pet_id,
            start_date=date,
            end_date=date
        )
        if not summary:
            raise HTTPException(status_code=404, detail="No records found for this date")
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pet_id}/night")
async def get_night_calories(
        pet_id: str,
        date,
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get night time calories summary"""
    try:
        summary = await calories_service.night_calories(
            db=db,
            pet_id=pet_id,
            start_date=date,
            end_date=date
        )
        if not summary:
            raise HTTPException(status_code=404, detail="No records found for this period")
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pet_id}/daytime")
async def get_daytime_calories(
        pet_id: str,
        date: str,
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get daytime calories summary"""
    try:
        summary = await calories_service.daytime_calories(
            db=db,
            pet_id=pet_id,
            start_date=date,
            end_date=date
        )
        if not summary:
            raise HTTPException(status_code=404, detail="No records found for this period")
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pet_id}/weekly")
async def get_weekly_calories(
        pet_id: str,
        start_date: str,
        end_date: str,
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get weekly calories summary"""
    try:
        summary = await calories_service.weekly_calories(
            db=db,
            pet_id=pet_id,
            start_date=start_date,
            end_date=end_date
        )
        if not summary:
            raise HTTPException(status_code=404, detail="No records found for this period")
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pet_id}/monthly")
async def get_monthly_calories(
        pet_id: str,
        date: str,
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get monthly calories summary"""
    try:
        summary = await calories_service.monthly_calories(
            db=db,
            pet_id=pet_id,
            start_date=date,
            end_date=date
        )
        if not summary:
            raise HTTPException(status_code=404, detail="No records found for this period")
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pet_id}/yearly")
async def get_yearly_calories(
        pet_id: str,
        date: str,
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get yearly calories summary"""
    try:
        summary = await calories_service.yearly_calories(
            db=db,
            pet_id=pet_id,
            start_date=date,
            end_date=date
        )
        if not summary:
            raise HTTPException(status_code=404, detail="No records found for this period")
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))