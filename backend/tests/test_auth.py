def test_valid_admin_login(client):
    response = client.post("/api/auth/login", json={
        "email": "admin@lms.com",
        "password": "Admin@123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["role"]["name"] == "admin"

def test_invalid_password(client):
    response = client.post("/api/auth/login", json={
        "email": "admin@lms.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_nonexistent_user(client):
    response = client.post("/api/auth/login", json={
        "email": "ghost@lms.com",
        "password": "SomePassword123"
    })
    assert response.status_code == 401

def test_get_current_user_profile(client, student_token):
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "student1@lms.com"
    assert data["role"]["name"] == "student"

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "online"]
    assert data["database"] == "connected"
