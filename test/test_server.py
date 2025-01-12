import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_server_is_running(client):
    response = client.get("/")  # root endpoint 테스트
    assert response.status_code == 200
