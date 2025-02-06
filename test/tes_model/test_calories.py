import pytest
from datetime import datetime, timedelta
from bson import ObjectId
from models.calories import PetcaloriesCollection

# 테스트용 데이터를 생성하는 fixture
@pytest.fixture
async def test_db(monkeypatch):
    class MockCollection:
        async def aggregate(self, pipeline):
            class MockCursor:
                async def to_list(self, length):
                    # 테스트용 데이터 반환
                    return [{
                        "_id": ObjectId(),
                        "avg_calories": 250.5,
                        "max_calories": 350.0,
                        "max_calories_time": "14:30",
                        "min_calories": 150.0,
                        "min_calories_time": "08:15"
                    }]
            return MockCursor()

        async def create_index(self, index):
            return None

    class MockDB:
        def __getitem__(self, name):
            return MockCollection()

    return MockDB()

@pytest.mark.asyncio
async def test_get_pet_calories_daily_history(test_db):
    # 테스트 데이터 설정
    pet_id = str(ObjectId())
    start_date = datetime.now()
    end_date = start_date + timedelta(days=1)

    # 함수 실행
    result = await PetcaloriesCollection.get_pet_calories_daily_history(
        test_db,
        pet_id,
        start_date,
        end_date
    )

    # 결과 검증
    assert result is not None
    assert "avg_calories" in result
    assert "max_calories" in result
    assert "min_calories" in result
    assert "max_calories_time" in result
    assert "min_calories_time" in result
    # 시간 형식 검증 (HH:MM)
    assert len(result["max_calories_time"]) == 5
    assert ":" in result["max_calories_time"]

@pytest.mark.asyncio
async def test_get_pet_calories_weekly_history(test_db):
    pet_id = str(ObjectId())
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)

    result = await PetcaloriesCollection.get_pet_calories_weekly_history(
        test_db,
        pet_id,
        start_date,
        end_date
    )

    assert result is not None
    assert "avg_calories" in result
    assert "max_calories" in result
    assert "min_calories" in result
    # 날짜 형식 검증 (YYYY-MM-DD)
    assert len(result["max_calories_time"]) == 10
    assert result["max_calories_time"].count("-") == 2

@pytest.mark.asyncio
async def test_get_pet_calories_monthly_history(test_db):
    pet_id = str(ObjectId())
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)

    result = await PetcaloriesCollection.get_pet_calories_monthly_history(
        test_db,
        pet_id,
        start_date,
        end_date
    )

    assert result is not None
    assert "avg_calories" in result
    assert "max_calories" in result
    assert "min_calories" in result
    # 주차 형식 검증
    assert result["max_calories_time"].endswith("주차")
    assert result["min_calories_time"].endswith("주차")

@pytest.mark.asyncio
async def test_get_pet_calories_yearly_history(test_db):
    pet_id = str(ObjectId())
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365)

    result = await PetcaloriesCollection.get_pet_calories_yearly_history(
        test_db,
        pet_id,
        start_date,
        end_date
    )

    assert result is not None
    assert "avg_calories" in result
    assert "max_calories" in result
    assert "min_calories" in result
    # 월 형식 검증
    assert result["max_calories_time"].endswith("월")
    assert result["min_calories_time"].endswith("월")

@pytest.mark.asyncio
async def test_empty_results(test_db):
    # Mock 데이터를 None으로 반환하도록 수정
    class EmptyMockCollection:
        async def aggregate(self, pipeline):
            class MockCursor:
                async def to_list(self, length):
                    return []
            return MockCursor()

    class EmptyMockDB:
        def __getitem__(self, name):
            return EmptyMockCollection()

    pet_id = str(ObjectId())
    start_date = datetime.now()
    end_date = start_date + timedelta(days=1)

    result = await PetcaloriesCollection.get_pet_calories_daily_history(
        EmptyMockDB(),
        pet_id,
        start_date,
        end_date
    )

    assert result is None

@pytest.mark.asyncio
async def test_date_range_validation():
    pet_id = str(ObjectId())
    end_date = datetime.now()
    start_date = end_date + timedelta(days=1)  # 시작일이 종료일보다 늦은 경우

    # 이 테스트는 실패해야 함
    with pytest.raises(Exception):
        await PetcaloriesCollection.get_pet_calories_daily_history(
            test_db,
            pet_id,
            start_date,
            end_date
        )