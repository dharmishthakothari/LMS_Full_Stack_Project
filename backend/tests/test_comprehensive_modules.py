import pytest
from fastapi import HTTPException
from app.middleware.rate_limit import DatabaseRateLimiter


def test_db_backed_rate_limiter_persists_and_blocks(db_session):
    """Verify DatabaseRateLimiter persists hit counts in DB and raises 429 above threshold."""
    limiter = DatabaseRateLimiter(max_requests=3, window_seconds=60)
    key = "test:client-ip-1"

    limiter.check(key, db_session)
    limiter.check(key, db_session)
    limiter.check(key, db_session)

    with pytest.raises(HTTPException) as exc_info:
        limiter.check(key, db_session)
    assert exc_info.value.status_code == 429


def test_communications_announcements_and_notifications(client, admin_token, student_token):
    """Test announcement creation RBAC and notification read-all workflow."""
    # Student cannot post announcements
    forbidden = client.post(
        "/api/announcements",
        json={"title": "Test", "content": "Unauthorized", "target_role": "all"},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert forbidden.status_code == 403

    # Admin can post announcement
    created = client.post(
        "/api/announcements",
        json={"title": "Exam Schedule", "content": "Finals next week", "target_role": "all"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert created.status_code in [200, 201]
    assert created.json()["title"] == "Exam Schedule"

    # Student can list announcements and mark notifications read
    anns = client.get("/api/announcements", headers={"Authorization": f"Bearer {student_token}"})
    assert anns.status_code == 200
    assert any(a["title"] == "Exam Schedule" for a in anns.json())

    notifs = client.get("/api/notifications", headers={"Authorization": f"Bearer {student_token}"})
    assert notifs.status_code == 200

    read_all = client.put("/api/notifications/read-all", headers={"Authorization": f"Bearer {student_token}"})
    assert read_all.status_code == 200


def test_reports_dashboard_and_csv_export(client, admin_token, instructor_token, student_token):
    """Test analytics dashboard across roles and CSV export endpoint."""
    for token in (admin_token, instructor_token, student_token):
        resp = client.get("/api/reports/dashboard", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200

    csv_resp = client.get("/api/reports/export/csv", headers={"Authorization": f"Bearer {admin_token}"})
    assert csv_resp.status_code == 200
    assert "text/csv" in csv_resp.headers.get("content-type", "")

    # Student forbidden from admin CSV export
    student_csv = client.get("/api/reports/export/csv", headers={"Authorization": f"Bearer {student_token}"})
    assert student_csv.status_code == 403


def test_lectures_and_progress_me(client, student_token):
    """Test listing lectures, completing a lecture, and fetching personal progress."""
    lectures = client.get("/api/lectures", headers={"Authorization": f"Bearer {student_token}"})
    assert lectures.status_code == 200
    data = lectures.json()
    assert len(data) > 0

    first_id = data[0]["id"]
    complete_resp = client.post(
        f"/api/lectures/{first_id}/complete",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert complete_resp.status_code == 200

    prog = client.get("/api/progress/me", headers={"Authorization": f"Bearer {student_token}"})
    assert prog.status_code == 200


def test_batches_students_instructors_and_certificates(client, admin_token, student_token):
    """Test directory endpoints and certificate verification error handling."""
    batches = client.get("/api/batches", headers={"Authorization": f"Bearer {admin_token}"})
    assert batches.status_code == 200
    assert len(batches.json()) > 0

    students = client.get("/api/students", headers={"Authorization": f"Bearer {admin_token}"})
    assert students.status_code == 200
    assert len(students.json()) > 0

    instructors = client.get("/api/instructors", headers={"Authorization": f"Bearer {admin_token}"})
    assert instructors.status_code == 200
    assert len(instructors.json()) > 0

    certs = client.get("/api/certificates", headers={"Authorization": f"Bearer {student_token}"})
    assert certs.status_code == 200

    bad_verify = client.get("/api/certificates/verify/NONEXISTENT-CERT-XYZ")
    assert bad_verify.status_code == 404
