import pytest
import os
import sys

# Ensure backend root is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, SessionLocal
from app.models import User

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="session")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_auth_token(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, f"Failed to login {email}: {response.text}"
    return response.json()["access_token"]

@pytest.fixture(scope="session")
def admin_token(client):
    return get_auth_token(client, "admin@lms.com", "Admin@123")

@pytest.fixture(scope="session")
def instructor_token(client):
    return get_auth_token(client, "dr.patel@lms.com", "Instructor@123")

@pytest.fixture(scope="session")
def student_token(client):
    return get_auth_token(client, "student1@lms.com", "Student@123")
