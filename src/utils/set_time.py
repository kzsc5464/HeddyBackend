from datetime import datetime, date, timedelta
from typing import List, Optional

def convert_to_month_week(year, year_week) -> str:
    """
    연도의 주차를 해당 월의 주차로 변환
    예: "51주차" -> "3주차" (12월의 경우)
    mongodb에서 51주차처럼 전체 년월일에서 주차를 주기 떄문에 만들게되었음
    """
    try:
        # "51주차"에서 숫자만 추출
        week_number = year_week

        # 해당 연도와 주차로 날짜 계산 (예시로 2024년 사용)
        year = 2024  # 실제로는 현재 연도나 데이터의 연도를 사용해야 함
        first_day = datetime(year, 1, 1)
        target_date = first_day + timedelta(weeks=(week_number - 1))

        # 해당 날짜의 월 주차 계산
        month_week = get_month_week(target_date)
        print(month_week)
        return month_week
    except Exception as e:
        print(f"Error converting week format: {e}")
        return year_week


def get_month_week(date):
    """
        한국식 주차 계산 (매월 1일이 포함된 주가 1주차)
        사용하지 않지만 일단 준비
    """
    date = datetime.strptime(date, "%Y-%m-%d")
    first_day = date.replace(day=1)  # 해당 월의 1일
    first_day_weekday = first_day.weekday()  # 1일의 요일 (0=월요일, 6=일요일)
    day_of_month = date.day  # 입력된 날짜의 일자

    # 1일이 속한 첫 주에 며칠이 있는지 계산
    days_in_first_week = 7 - first_day_weekday

    if day_of_month <= days_in_first_week:
        # 첫 주에 속하는 경우
        return 1
    else:
        # 첫 주 이후의 날짜는 남은 일수를 7로 나누어 계산
        remaining_days = day_of_month - days_in_first_week
        return (remaining_days - 1) // 7 + 2  # 2주차부터 시작

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
