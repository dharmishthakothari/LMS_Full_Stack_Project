import uuid

def test_list_courses(client, student_token):
    response = client.get("/api/courses", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) >= 1

def test_create_course_admin(client, admin_token):
    code = f"TEST-{uuid.uuid4().hex[:5].upper()}"
    response = client.post("/api/courses", json={
        "title": "Automated Testing Course",
        "code": code,
        "category": "Quality Assurance",
        "description": "Comprehensive automated testing and verification.",
        "duration_weeks": 8,
        "fee": 15000.0,
        "status": "published"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["code"] == code

def test_batch_date_validation(client, admin_token):
    # End date preceding start date must be rejected with 400
    response = client.post("/api/batches", json={
        "name": "Invalid Date Batch",
        "code": f"INV-{uuid.uuid4().hex[:4].upper()}",
        "course_id": 1,
        "start_date": "2026-12-01",
        "end_date": "2026-11-01",
        "class_days": "Mon, Wed",
        "class_timing": "10:00 AM",
        "capacity": 20,
        "status": "upcoming"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 400
    assert "End date cannot precede start date" in response.json()["detail"]
