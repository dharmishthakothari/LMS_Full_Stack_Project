def test_student_forbidden_from_users_list(client, student_token):
    response = client.get("/api/users", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

def test_instructor_forbidden_from_creating_user(client, instructor_token):
    response = client.post("/api/users", json={
        "email": "new.test.user@lms.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User",
        "role_name": "student"
    }, headers={"Authorization": f"Bearer {instructor_token}"})
    assert response.status_code == 403

def test_student_forbidden_from_recording_payments(client, student_token):
    response = client.post("/api/payments", json={
        "student_id": 1,
        "course_id": 1,
        "paid_amount": 5000.0,
        "payment_method": "UPI",
        "transaction_reference": "TXN-FAKE-123"
    }, headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 403

def test_admin_allowed_to_view_all_users(client, admin_token):
    response = client.get("/api/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 4
