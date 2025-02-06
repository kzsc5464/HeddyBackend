from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from models.pet import PetType

class CaloriesBase(BaseModel):
    """Base calories response schema"""
    avg_calories: float = Field(..., description="평균 칼로리")
    max_calories: float = Field(..., description="최대 칼로리")
    min_calories: float = Field(..., description="최소 칼로리")
    max_calories_time: str = Field(..., description="최대 칼로리 기록 시간")
    min_calories_time: str = Field(..., description="최소 칼로리 기록 시간")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "avg_calories": 148.33,
                "max_calories": 210.0,
                "min_calories": 35.0,
                "max_calories_time": "14:30",
                "min_calories_time": "08:15"
            }
        }
    )

class DailyCaloriesResponse(CaloriesBase):
    """Daily calories response with HH:MM time format"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "avg_calories": 148.33,
                "max_calories": 210.0,
                "min_calories": 35.0,
                "max_calories_time": "14:30",
                "min_calories_time": "08:15"
            }
        }
    )

class WeeklyCaloriesResponse(CaloriesBase):
    """Weekly calories response with YYYY-MM-DD date format"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "avg_calories": 148.33,
                "max_calories": 210.0,
                "min_calories": 35.0,
                "max_calories_time": "2024-01-15",
                "min_calories_time": "2024-01-12"
            }
        }
    )

class MonthlyCaloriesResponse(CaloriesBase):
    """Monthly calories response with week number format"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "avg_calories": 148.33,
                "max_calories": 210.0,
                "min_calories": 35.0,
                "max_calories_time": "3주차",
                "min_calories_time": "1주차"
            }
        }
    )

class YearlyCaloriesResponse(CaloriesBase):
    """Yearly calories response with month format"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "avg_calories": 148.33,
                "max_calories": 210.0,
                "min_calories": 35.0,
                "max_calories_time": "7월",
                "min_calories_time": "3월"
            }
        }
    )

class CaloriesRequest(BaseModel):
    """Request schema for calories endpoints"""
    pet_id: str = Field(..., description="반려동물 ID")
    start_date: str = Field(..., description="시작 날짜 (YYYY-MM-DD 또는 YYYY-MM)")
    end_date: str = Field(..., description="종료 날짜 (YYYY-MM-DD 또는 YYYY-MM)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pet_id": "pet123",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31"
            }
        }
    )

# API 응답을 위한 통합 스키마
class CaloriesResponseModel(BaseModel):
    """Generic response wrapper for calories data"""
    status: str = Field(default="success", description="응답 상태")
    message: Optional[str] = Field(None, description="응답 메시지")
    data: Optional[CaloriesBase] = Field(None, description="칼로리 데이터")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "message": "Successfully retrieved calories data",
                "data": {
                    "avg_calories": 148.33,
                    "max_calories": 210.0,
                    "min_calories": 35.0,
                    "max_calories_time": "14:30",
                    "min_calories_time": "08:15"
                }
            }
        }
    )