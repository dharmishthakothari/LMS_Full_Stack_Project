from typing import Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models import (
    Student, Course, Batch, Enrollment, Lecture, CourseModule,
    LectureProgress, Assignment, Submission, Quiz, QuizAttempt,
    Attendance, Payment
)

def calculate_student_course_progress(db: Session, student_id: int, course_id: int) -> Dict[str, Any]:
    student = db.query(Student).filter(Student.id == student_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()
    if not student or not course:
        return {}

    # 1. Lectures
    total_lectures = (
        db.query(Lecture)
        .join(CourseModule)
        .filter(CourseModule.course_id == course_id)
        .count()
    )
    completed_lectures = (
        db.query(LectureProgress)
        .join(Lecture)
        .join(CourseModule)
        .filter(
            LectureProgress.student_id == student_id,
            LectureProgress.is_completed == True,
            CourseModule.course_id == course_id
        )
        .count()
    )
    lecture_pct = (completed_lectures / total_lectures * 100.0) if total_lectures > 0 else 0.0

    # 2. Batches student is enrolled in for this course
    enrolled_batches = (
        db.query(Batch.id)
        .join(Enrollment, Enrollment.batch_id == Batch.id)
        .filter(
            Batch.course_id == course_id,
            Enrollment.student_id == student_id,
            Enrollment.status == "active"
        )
        .all()
    )
    batch_ids = [b[0] for b in enrolled_batches]

    # 3. Assignments
    if batch_ids:
        total_assignments = db.query(Assignment).filter(Assignment.batch_id.in_(batch_ids)).count()
        evaluated_assignments = (
            db.query(Submission)
            .join(Assignment)
            .filter(
                Assignment.batch_id.in_(batch_ids),
                Submission.student_id == student_id,
                Submission.status == "evaluated"
            )
            .count()
        )
    else:
        total_assignments = 0
        evaluated_assignments = 0
    assignment_pct = (evaluated_assignments / total_assignments * 100.0) if total_assignments > 0 else 0.0

    # 4. Quizzes
    if batch_ids:
        total_quizzes = db.query(Quiz).filter(Quiz.batch_id.in_(batch_ids), Quiz.is_published == True).count()
        passed_quizzes = (
            db.query(QuizAttempt)
            .join(Quiz)
            .filter(
                Quiz.batch_id.in_(batch_ids),
                QuizAttempt.student_id == student_id,
                QuizAttempt.is_passed == True
            )
            .count()
        )
    else:
        total_quizzes = 0
        passed_quizzes = 0
    quiz_pct = (passed_quizzes / total_quizzes * 100.0) if total_quizzes > 0 else 0.0

    # 5. Attendance
    if batch_ids:
        total_sessions = db.query(Attendance).filter(Attendance.batch_id.in_(batch_ids), Attendance.student_id == student_id).count()
        present_sessions = db.query(Attendance).filter(
            Attendance.batch_id.in_(batch_ids),
            Attendance.student_id == student_id,
            Attendance.status == "present"
        ).count()
    else:
        total_sessions = 0
        present_sessions = 0
    attendance_pct = (present_sessions / total_sessions * 100.0) if total_sessions > 0 else 100.0

    # 6. Overall Weighted Progress
    overall_progress = (0.40 * lecture_pct) + (0.30 * assignment_pct) + (0.30 * quiz_pct)

    # 7. Fee check
    payment_record = db.query(Payment).filter(Payment.student_id == student_id, Payment.course_id == course_id).first()
    has_pending_fee = False
    if payment_record and payment_record.pending_amount > Decimal("0.00"):
        has_pending_fee = True

    is_eligible = (overall_progress >= 80.0) and (attendance_pct >= 75.0) and (not has_pending_fee)

    return {
        "student_id": student.id,
        "student_name": f"{student.user.first_name} {student.user.last_name}",
        "course_id": course.id,
        "course_title": course.title,
        "completed_lectures": completed_lectures,
        "total_lectures": total_lectures,
        "lecture_completion_percentage": round(lecture_pct, 1),
        "evaluated_assignments": evaluated_assignments,
        "total_assignments": total_assignments,
        "assignment_completion_percentage": round(assignment_pct, 1),
        "passed_quizzes": passed_quizzes,
        "total_quizzes": total_quizzes,
        "quiz_completion_percentage": round(quiz_pct, 1),
        "attendance_percentage": round(attendance_pct, 1),
        "overall_progress_percentage": round(overall_progress, 1),
        "is_eligible_for_certificate": is_eligible
    }
