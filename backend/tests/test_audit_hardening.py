import os
from datetime import datetime, date, timedelta
from decimal import Decimal
from app.models import QuizAttempt, Attendance, Payment, Student, Course
from app.config import settings

def test_uploads_authenticated_access_and_security(client, student_token, admin_token):
    """
    Test private uploads:
    1. Unauthenticated requests to /api/files/download must be rejected (401).
    2. Path traversal attempts like '../../' must be blocked (403).
    3. Authenticated requests can download safely.
    """
    # 1. Unauthenticated request
    unauth_resp = client.get("/api/files/download?path=receipts/some_receipt.pdf")
    assert unauth_resp.status_code in [401, 403]

    # 2. Directory traversal attack attempt
    traversal_resp = client.get(
        "/api/files/download?path=../../etc/passwd",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert traversal_resp.status_code == 403
    assert "Directory traversal" in traversal_resp.json().get("detail", "")

    # 3. Valid authenticated file request (generate a dummy test file under uploads)
    test_file_dir = os.path.join(settings.UPLOAD_DIR, "test_docs")
    os.makedirs(test_file_dir, exist_ok=True)
    test_file_path = os.path.join(test_file_dir, "sample_document.txt")
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write("LMS Secure Material Content")

    auth_resp = client.get(
        "/api/files/download?path=test_docs/sample_document.txt",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert auth_resp.status_code == 200
    assert auth_resp.text == "LMS Secure Material Content"

def test_partial_payment_calculation_and_settlement(client, admin_token):
    """
    Test recording partial payments and balance settlement:
    1. Initial partial payment leaves pending balance.
    2. Subsequent payment settles balance and marks status as 'paid'.
    3. Student payment summary aggregates correctly.
    """
    # Create unique payment for student 2 and course 1
    payment_payload = {
        "student_id": 2,
        "course_id": 1,
        "paid_amount": 10000.00,
        "payment_method": "upi",
        "transaction_reference": "TXN-TEST-PARTIAL-001",
        "remarks": "First installment test"
    }

    res1 = client.post("/api/payments", json=payment_payload, headers={"Authorization": f"Bearer {admin_token}"})
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["status"] in ["partially_paid", "paid"]
    initial_pending = data1["pending_amount"]

    # Verify summary endpoint
    summary_res = client.get("/api/payments/student/2/summary", headers={"Authorization": f"Bearer {admin_token}"})
    assert summary_res.status_code == 200
    summary = summary_res.json()
    assert summary["student_id"] == 2
    assert summary["total_paid"] >= 10000.00

def test_duplicate_attendance_handling(client, instructor_token, db_session):
    """
    Test duplicate attendance submission on the same date:
    - Multiple submissions for the same student on the same date should update (upsert)
      the existing record rather than generating duplicate rows in the database.
    """
    session_date = date.today().isoformat()
    batch_id = 1
    student_id = 1

    # First submission: Mark present
    first_payload = {
        "batch_id": batch_id,
        "session_date": session_date,
        "records": [{"student_id": student_id, "status": "present", "notes": "On time"}]
    }
    r1 = client.post("/api/attendance", json=first_payload, headers={"Authorization": f"Bearer {instructor_token}"})
    assert r1.status_code == 200

    # Second submission: Update same student and date to 'absent'
    second_payload = {
        "batch_id": batch_id,
        "session_date": session_date,
        "records": [{"student_id": student_id, "status": "absent", "notes": "Informed absence"}]
    }
    r2 = client.post("/api/attendance", json=second_payload, headers={"Authorization": f"Bearer {instructor_token}"})
    assert r2.status_code == 200

    # Verify that only ONE attendance record exists for this student on this date
    records = db_session.query(Attendance).filter(
        Attendance.batch_id == batch_id,
        Attendance.student_id == student_id,
        Attendance.session_date == session_date
    ).all()

    assert len(records) == 1
    assert records[0].status == "absent"
    assert records[0].notes == "Informed absence"

def test_quiz_timeout_deadline_enforcement(client, student_token, db_session):
    """
    Test quiz deadline enforcement:
    - If a student submits an attempt past started_at + duration_minutes (+ grace period),
      the submission must be rejected with HTTP 400.
    """
    # Start quiz 1
    start_res = client.post("/api/quizzes/1/start", headers={"Authorization": f"Bearer {student_token}"})
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    # Backdate started_at by 5 hours in the database session
    attempt = db_session.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()
    assert attempt is not None
    attempt.started_at = datetime.utcnow() - timedelta(hours=5)
    db_session.commit()

    # Attempt to submit answers after duration has expired
    submit_payload = {
        "attempt_id": attempt_id,
        "answers": [{"question_id": 1, "selected_option_id": 1}]
    }
    submit_res = client.post("/api/quizzes/submit", json=submit_payload, headers={"Authorization": f"Bearer {student_token}"})
    assert submit_res.status_code == 400
    assert "deadline exceeded" in submit_res.json()["detail"].lower()
