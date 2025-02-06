from datetime import datetime
from typing import Dict, Any
from calendar import monthrange
from models.calories import PetcaloriesCollection
from utils.set_time import get_month_week

class PetCaloriesService:
    @staticmethod
    def _convert_date_range(raw_start_date: str, raw_end_date: str) -> tuple[datetime, datetime]:
        """Convert dates to start of day and end of day format."""
        start_date = datetime.strptime(raw_start_date, "%Y-%m-%d")
        end_date = datetime.strptime(raw_end_date, "%Y-%m-%d")
        start_date = datetime(start_date.year, start_date.month, start_date.day)
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        return start_date, end_date

    @staticmethod
    def _convert_date_range_daytime(start_date: str, end_date: str) -> tuple[datetime, datetime]:
        """Convert dates to start of day and end of day format."""
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = datetime(start_date.year, start_date.month, start_date.day,6,0,0,)
        end_date = datetime(end_date.year, end_date.month, end_date.day, 18, 0, 0)
        return start_date, end_date

    @staticmethod
    def _convert_date_range_night(start_date: str, end_date: str) -> tuple[datetime, datetime]:
        """Convert dates to start of day and end of day format."""
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = datetime(start_date.year, start_date.month, start_date.day, 18,0,0)
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59,999)
        return start_date, end_date

    @staticmethod
    def _convert_date_monthily(raw_start_date: str, raw_end_date: str) -> tuple[datetime, datetime]:
        start_date = datetime.strptime(raw_start_date, "%Y-%m")
        end_date = datetime.strptime(raw_end_date, "%Y-%m")
        _, last_day = monthrange(end_date.year, end_date.month)
        start_month = datetime(start_date.year, start_date.month,1)
        end_month = datetime(end_date.year, end_date.month,last_day)
        return start_month, end_month

    @staticmethod
    def _convert_date_yealy(raw_start_date: str, raw_end_date: str) -> tuple[datetime, datetime]:
        start_date = datetime.strptime(raw_start_date, "%Y")
        end_date = datetime.strptime(raw_end_date, "%Y")
        _, last_day = monthrange(end_date.year, end_date.month)
        start_month = datetime(start_date.year, 1,31)
        end_month = datetime(end_date.year, 12,31)
        return start_month, end_month

    async def _get_calories_history(
        self,
        db: Any,
        pet_id: str,
        start_date: str,
        end_date: str,
        history_type: str = "daily"
    ) -> Dict:
        """Base method for retrieving calories history."""
        if history_type == "daily":
            start_date, end_date = self._convert_date_range(start_date, end_date)
        elif history_type == "daytime":
            start_date, end_date = self._convert_date_range_daytime(start_date, end_date)
        elif history_type == "night":
            start_date, end_date = self._convert_date_range_night(start_date, end_date)
        elif history_type == "monthly":
            start_date, end_date = self._convert_date_monthily(start_date, end_date)
        elif history_type == "yearly":
            start_date, end_date = self._convert_date_yealy(start_date, end_date)
        else:
            start_date, end_date = self._convert_date_range(start_date, end_date)

        print(start_date)

        collection_methods = {
            "daily": PetcaloriesCollection.get_pet_calories_daily_history,
            "daytime": PetcaloriesCollection.get_pet_calories_daily_history,
            "night": PetcaloriesCollection.get_pet_calories_daily_history,
            "weekly": PetcaloriesCollection.get_pet_calories_weekly_history,
            "monthly": PetcaloriesCollection.get_pet_calories_monthly_history,
            "yearly": PetcaloriesCollection.get_pet_calories_yearly_history
        }

        method = collection_methods.get(history_type)
        if not method:
            raise ValueError(f"Invalid history type: {history_type}")

        results = await method(
            db=db,
            pet_id=pet_id,
            start_date=start_date,
            end_date=end_date,
        )

        return results if results else {}

    async def daytime_calories(
        self,
        db: Any,
        pet_id: str,
        start_date: str,
        end_date: str
    ) -> Dict:
        return await self._get_calories_history(
            db,
            pet_id,
            start_date,
            end_date,
            "daytime"
        )

    async def night_calories(
        self,
        db: Any,
        pet_id: str,
        start_date: str,
        end_date: str
    ) -> Dict:
        return await self._get_calories_history(
            db,
            pet_id,
            start_date,
            end_date,
            "night"
        )

    async def daily_calories(
        self,
        db: Any,
        pet_id: str,
        start_date: str,
        end_date: str
    ) -> Dict:
        return await self._get_calories_history(
            db,
            pet_id,
            start_date,
            end_date,
            "daily"
        )

    async def weekly_calories(
        self,
        db: Any,
        pet_id: str,
        start_date: str,
        end_date: str
    ) -> Dict:
        return await self._get_calories_history(
            db,
            pet_id,
            start_date,
            end_date,
            "weekly"
        )


    async def monthly_calories(
        self,
        db: Any,
        pet_id: str,
        start_date,
        end_date
    ) -> Dict:
        results = await self._get_calories_history(
            db,
            pet_id,
            start_date,
            end_date,
            "monthly"
        )
        results["max_calories_time"] = get_month_week(results["max_calories_time"])
        results["min_calories_time"] = get_month_week(results["min_calories_time"])
        return results

    async def yearly_calories(
        self,
        db: Any,
        pet_id: str,
        start_date,
        end_date,
    ) -> Dict:
        return await self._get_calories_history(
            db,
            pet_id,
            start_date,
            end_date,
            "yearly"
        )