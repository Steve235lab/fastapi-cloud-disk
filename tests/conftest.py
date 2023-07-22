import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import api_router


@pytest.fixture(scope="session")
def get_test_client() -> TestClient:
    app = FastAPI()
    app.include_router(api_router)
    test_client = TestClient(app)
    test_client.post("api/user/login", json={"username": "DEV_USER", "password": "DEV_PWD"})
    return test_client
