from datetime import datetime, date, timedelta
from typing import List, Optional

def convert_date_to_datetime_range(
                                   raw_startdate: Optional[str],
                                   raw_enddate: Optional[str]
    ) -> tuple[Optional[datetime], Optional[datetime]]:
    if not raw_startdate:
        return None, None

    try:
        # 날짜 문자열을 datetime 객체로 변환 (YYYY-MM-DD 형식 가정)
        start_base_date = datetime.strptime(raw_startdate, "%Y-%m-%d")
        end_base_date = datetime.strptime(raw_enddate, "%Y-%m-%d")

        # 시작 시간 (00:00:00)
        start_datetime = start_base_date

        # 종료 시간 (23:59:59)
        end_datetime = end_base_date + timedelta(days=1) - timedelta(seconds=1)

        return start_datetime, end_datetime

    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

def convert_date_afternonn(
                            raw_startdate: Optional[str],
                            raw_enddate: Optional[str]
    ) -> tuple[Optional[datetime], Optional[datetime]]:
    try:
        # 날짜 문자열을 datetime 객체로 변환 (YYYY-MM-DD 형식 가정)
        start_base_date = datetime.strptime(raw_startdate, "%Y-%m-%d")
        end_base_date = datetime.strptime(raw_enddate, "%Y-%m-%d")

        # 시작 시간 (06:00:00)
        start_datetime = start_base_date + timedelta(hours=6)

        # 종료 시간 (18:00:00)
        end_datetime = end_base_date + timedelta(hours=18)

        return start_datetime, end_datetime

    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

def conver_date_night(
                    raw_startdate: Optional[str],
                    raw_enddate: Optional[str]
    ) -> tuple[Optional[datetime], Optional[datetime]]:
    try:
        # 날짜 문자열을 datetime 객체로 변환 (YYYY-MM-DD 형식 가정)
        start_base_date = datetime.strptime(raw_startdate, "%Y-%m-%d")
        end_base_date = datetime.strptime(raw_enddate, "%Y-%m-%d")

        # 시작 시간 (18:00:00)
        start_datetime = start_base_date + timedelta(hours=6)

        # 종료 시간 (23:59:59)
        end_datetime = end_base_date + timedelta(days=1) - timedelta(seconds=1)

        return start_datetime, end_datetime

    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
