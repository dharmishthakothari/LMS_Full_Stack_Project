from datetime import datetime, timedelta
from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Quiz, Question, QuizOption, QuizAttempt, QuizAnswer, Batch, User, Enrollment
from app.schemas.quiz import QuizCreate, SubmitQuizRequest, AttemptResultResponse
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/api/quizzes", tags=["Quizzes"])

@router.get("")
def list_quizzes(
    batch_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Quiz)

    if current_user.role.name == "student" and current_user.student_profile:
        enrolled_batches = db.query(Enrollment.batch_id).filter(
            Enrollment.student_id == current_user.student_profile.id,
            Enrollment.status == "active"
        ).all()
        b_ids = [b[0] for b in enrolled_batches]
        query = query.filter(Quiz.batch_id.in_(b_ids), Quiz.is_published == True)
    elif current_user.role.name == "instructor" and current_user.instructor_profile:
        inst_batches = db.query(Batch.id).filter(Batch.instructor_id == current_user.instructor_profile.id).all()
        b_ids = [b[0] for b in inst_batches]
        query = query.filter(Quiz.batch_id.in_(b_ids))

    if batch_id:
        query = query.filter(Quiz.batch_id == batch_id)

    quizzes = query.order_by(Quiz.id.desc()).all()
    results = []

    for q in quizzes:
        my_attempts = 0
        best_score = None
        is_passed = False

        if current_user.role.name == "student" and current_user.student_profile:
            attempts = db.query(QuizAttempt).filter(
                QuizAttempt.quiz_id == q.id,
                QuizAttempt.student_id == current_user.student_profile.id
            ).all()
            my_attempts = len(attempts)
            if attempts:
                best_score = max(float(att.score) for att in attempts)
                is_passed = any(att.is_passed for att in attempts)

        results.append({
            "id": q.id,
            "batch_id": q.batch_id,
            "batch_name": q.batch.name if q.batch else "",
            "course_title": q.batch.course.title if (q.batch and q.batch.course) else "",
            "title": q.title,
            "description": q.description,
            "duration_minutes": q.duration_minutes,
            "total_marks": q.total_marks,
            "passing_marks": q.passing_marks,
            "retake_allowed": q.retake_allowed,
            "max_attempts": q.max_attempts,
            "start_time": q.start_time.isoformat() if q.start_time else None,
            "end_time": q.end_time.isoformat() if q.end_time else None,
            "is_published": q.is_published,
            "questions_count": len(q.questions),
            "my_attempts_count": my_attempts,
            "highest_score": best_score,
            "is_passed": is_passed
        })
    return results

@router.post("")
def create_quiz(
    data: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    batch = db.query(Batch).filter(Batch.id == data.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found.")

    quiz = Quiz(
        batch_id=data.batch_id,
        title=data.title,
        description=data.description,
        duration_minutes=data.duration_minutes,
        total_marks=data.total_marks,
        passing_marks=data.passing_marks,
        retake_allowed=data.retake_allowed,
        max_attempts=data.max_attempts,
        start_time=data.start_time,
        end_time=data.end_time,
        is_published=data.is_published
    )
    db.add(quiz)
    db.flush()

    if data.questions:
        for q_in in data.questions:
            question = Question(
                quiz_id=quiz.id,
                question_text=q_in.question_text,
                marks=q_in.marks,
                sequence_order=q_in.sequence_order
            )
            db.add(question)
            db.flush()

            for opt_in in q_in.options:
                opt = QuizOption(
                    question_id=question.id,
                    option_text=opt_in.option_text,
                    is_correct=opt_in.is_correct
                )
                db.add(opt)

    db.commit()
    db.refresh(quiz)
    return {"message": "Quiz created successfully.", "quiz_id": quiz.id}

@router.get("/{quiz_id}")
def get_quiz_details(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    is_student = (current_user.role.name == "student")
    questions_data = []

    for q in quiz.questions:
        options_data = []
        for opt in q.options:
            opt_dict = {"id": opt.id, "option_text": opt.option_text}
            if not is_student:
                opt_dict["is_correct"] = opt.is_correct
            options_data.append(opt_dict)

        questions_data.append({
            "id": q.id,
            "question_text": q.question_text,
            "marks": q.marks,
            "sequence_order": q.sequence_order,
            "options": options_data
        })

    return {
        "id": quiz.id,
        "batch_id": quiz.batch_id,
        "title": quiz.title,
        "description": quiz.description,
        "duration_minutes": quiz.duration_minutes,
        "total_marks": quiz.total_marks,
        "passing_marks": quiz.passing_marks,
        "retake_allowed": quiz.retake_allowed,
        "max_attempts": quiz.max_attempts,
        "is_published": quiz.is_published,
        "questions": questions_data
    }

@router.post("/{quiz_id}/start")
def start_quiz_attempt(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["student"]))
):
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Student profile not found.")

    student_id = current_user.student_profile.id
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")
    if not quiz.is_published:
        raise HTTPException(status_code=400, detail="Quiz is not yet published.")

    # Enforce quiz scheduling window (start_time / end_time)
    now = datetime.utcnow()
    if quiz.start_time and now < quiz.start_time:
        raise HTTPException(
            status_code=400,
            detail=f"Quiz has not started yet. Opens at {quiz.start_time.isoformat()}."
        )
    if quiz.end_time and now > quiz.end_time:
        raise HTTPException(
            status_code=400,
            detail=f"Quiz window has closed. Ended at {quiz.end_time.isoformat()}."
        )

    # Check previous attempts
    past_attempts = db.query(QuizAttempt).filter(
        QuizAttempt.quiz_id == quiz_id,
        QuizAttempt.student_id == student_id
    ).all()

    if len(past_attempts) >= quiz.max_attempts and not quiz.retake_allowed:
        raise HTTPException(status_code=400, detail=f"Maximum allowed attempts ({quiz.max_attempts}) reached.")

    attempt = QuizAttempt(
        quiz_id=quiz_id,
        student_id=student_id,
        started_at=datetime.utcnow(),
        attempt_number=len(past_attempts) + 1
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "started_at": attempt.started_at.isoformat(),
        "duration_minutes": quiz.duration_minutes,
        "total_questions": len(quiz.questions)
    }

@router.post("/submit")
def submit_quiz_answers(
    req: SubmitQuizRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["student"]))
):
    attempt = db.query(QuizAttempt).filter(QuizAttempt.id == req.attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Quiz attempt not found.")
    if attempt.student_id != current_user.student_profile.id:
        raise HTTPException(status_code=403, detail="Unauthorized access to this quiz attempt.")
    if attempt.submitted_at:
        raise HTTPException(status_code=400, detail="This attempt has already been submitted.")

    now = datetime.utcnow()
    attempt.submitted_at = now

    # Server-side score calculation
    total_score = Decimal("0.00")
    for ans in req.answers:
        opt = db.query(QuizOption).filter(QuizOption.id == ans.selected_option_id).first()
        is_corr = False
        if opt and opt.is_correct and opt.question_id == ans.question_id:
            is_corr = True
            question = db.query(Question).filter(Question.id == ans.question_id).first()
            if question:
                total_score += Decimal(str(question.marks))

        quiz_ans = QuizAnswer(
            attempt_id=attempt.id,
            question_id=ans.question_id,
            selected_option_id=ans.selected_option_id,
            is_correct=is_corr
        )
        db.add(quiz_ans)

    attempt.score = total_score
    attempt.is_passed = (total_score >= Decimal(str(attempt.quiz.passing_marks)))
    db.commit()

    return {
        "message": "Quiz submitted and evaluated successfully.",
        "score": float(total_score),
        "total_marks": attempt.quiz.total_marks,
        "passing_marks": attempt.quiz.passing_marks,
        "is_passed": attempt.is_passed
    }

@router.get("/attempts/{attempt_id}")
def get_attempt_result(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    att = db.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()
    if not att:
        raise HTTPException(status_code=404, detail="Attempt not found.")

    if current_user.role.name == "student":
        if att.student_id != current_user.student_profile.id:
            raise HTTPException(status_code=403, detail="Access denied.")

    return {
        "id": att.id,
        "quiz_id": att.quiz_id,
        "quiz_title": att.quiz.title,
        "score": float(att.score),
        "total_marks": att.quiz.total_marks,
        "passing_marks": att.quiz.passing_marks,
        "is_passed": att.is_passed,
        "started_at": att.started_at.isoformat(),
        "submitted_at": att.submitted_at.isoformat() if att.submitted_at else None,
        "attempt_number": att.attempt_number
    }
