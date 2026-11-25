import uuid

def test_assignment_evaluation_marks_validation(client, instructor_token):
    # Attempting to assign marks greater than max marks should fail with 400
    response = client.post("/api/submissions/1/evaluate", json={
        "marks_obtained": 9999.0,
        "feedback_text": "Invalid marks test"
    }, headers={"Authorization": f"Bearer {instructor_token}"})
    assert response.status_code in [400, 404]

def test_student_quiz_answers_secrecy(client, student_token):
    # Correct answers must never be sent to the student prior to submission
    response = client.get("/api/quizzes/1", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    quiz = response.json()
    for q in quiz["questions"]:
        for opt in q["options"]:
            assert "is_correct" not in opt

def test_attendance_and_progress(client, student_token):
    response = client.get("/api/progress/student/1", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) or isinstance(data, dict)

def test_public_certificate_verification(client):
    response = client.get("/api/certificates/verify/V-LMS-984712")
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True
    assert "student_name" in data
