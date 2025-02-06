from datetime import datetime


def get_month_week(date):
    """
        한국식 주차 계산 (매월 1일이 포함된 주가 1주차)
    """
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

def test_isocalendar():
    date = datetime(2025,8,15)
    week_number = get_month_week(date)
    assert week_number == 3


if __name__ == '__main__':
    test_isocalendar()