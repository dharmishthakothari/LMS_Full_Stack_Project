import sys
import os
from datetime import datetime, date, timedelta
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import (
    Role, User, Instructor, Student, Course, CourseModule, Batch,
    Enrollment, Lecture, StudyMaterial, Assignment, Submission,
    AssignmentFeedback, Quiz, Question, QuizOption, QuizAttempt,
    QuizAnswer, Attendance, LectureProgress, Certificate, Payment,
    Notification, Announcement
)
from app.utils.security import get_password_hash

def seed():
    db = SessionLocal()
    print("Seeding database with synthetic records...")

    try:
        # 1. ROLES
        roles_data = [
            ("admin", "Administrator with full system privileges"),
            ("instructor", "Faculty member assigned to courses and batches"),
            ("student", "Enrolled student learner")
        ]
        role_map = {}
        for name, desc in roles_data:
            role = db.query(Role).filter_by(name=name).first()
            if not role:
                role = Role(name=name, description=desc)
                db.add(role)
                db.flush()
            role_map[name] = role

        # 2. USERS & PROFILES
        # Admin
        admin_email = "admin@lms.com"
        admin_user = db.query(User).filter_by(email=admin_email).first()
        if not admin_user:
            admin_user = User(
                role_id=role_map["admin"].id,
                email=admin_email,
                password_hash=get_password_hash("Admin@123"),
                first_name="Institute",
                last_name="Director",
                phone="+91 9876543210",
                is_active=True
            )
            db.add(admin_user)
            db.flush()

        # Instructors
        instructors_info = [
            ("dr.patel@lms.com", "Priya", "Patel", "+91 9811122233", "Full Stack Web Development & React", "Ph.D. in Computer Science"),
            ("er.verma@lms.com", "Amit", "Verma", "+91 9822233344", "Cloud Architecture & DevOps", "M.Tech in Software Engineering"),
            ("prof.sharma@lms.com", "Rajesh", "Sharma", "+91 9833344455", "Data Science & Applied ML", "Ph.D. in AI & Machine Learning")
        ]
        instructor_objs = []
        for email, fn, ln, ph, exp, qual in instructors_info:
            inst_user = db.query(User).filter_by(email=email).first()
            if not inst_user:
                inst_user = User(
                    role_id=role_map["instructor"].id,
                    email=email,
                    password_hash=get_password_hash("Instructor@123"),
                    first_name=fn,
                    last_name=ln,
                    phone=ph,
                    is_active=True
                )
                db.add(inst_user)
                db.flush()
            
            inst_profile = db.query(Instructor).filter_by(user_id=inst_user.id).first()
            if not inst_profile:
                inst_profile = Instructor(
                    user_id=inst_user.id,
                    expertise=exp,
                    qualification=qual,
                    biography=f"{qual} with over 10 years of industry and academic training experience."
                )
                db.add(inst_profile)
                db.flush()
            instructor_objs.append(inst_profile)

        # Students (10 students)
        students_info = [
            ("student1@lms.com", "Aarav", "Mehta", "+91 9100000001", "Mumbai, Maharashtra"),
            ("student2@lms.com", "Ananya", "Iyer", "+91 9100000002", "Bengaluru, Karnataka"),
            ("student3@lms.com", "Rohan", "Gupta", "+91 9100000003", "Delhi, NCR"),
            ("student4@lms.com", "Sneha", "Kulkarni", "+91 9100000004", "Pune, Maharashtra"),
            ("student5@lms.com", "Vikram", "Reddy", "+91 9100000005", "Hyderabad, Telangana"),
            ("student6@lms.com", "Pooja", "Nair", "+91 9100000006", "Kochi, Kerala"),
            ("student7@lms.com", "Karan", "Singhania", "+91 9100000007", "Ahmedabad, Gujarat"),
            ("student8@lms.com", "Diya", "Banerjee", "+91 9100000008", "Kolkata, West Bengal"),
            ("student9@lms.com", "Arjun", "Choudhury", "+91 9100000009", "Jaipur, Rajasthan"),
            ("student10@lms.com", "Riya", "Kapoor", "+91 9100000010", "Chandigarh, Punjab"),
        ]
        student_objs = []
        for email, fn, ln, ph, addr in students_info:
            stu_user = db.query(User).filter_by(email=email).first()
            if not stu_user:
                stu_user = User(
                    role_id=role_map["student"].id,
                    email=email,
                    password_hash=get_password_hash("Student@123"),
                    first_name=fn,
                    last_name=ln,
                    phone=ph,
                    is_active=True
                )
                db.add(stu_user)
                db.flush()

            stu_profile = db.query(Student).filter_by(user_id=stu_user.id).first()
            if not stu_profile:
                stu_profile = Student(
                    user_id=stu_user.id,
                    date_of_birth=date(2001, 5, 15),
                    address=addr,
                    emergency_contact="+91 9999988888",
                    joining_date=date.today() - timedelta(days=60)
                )
                db.add(stu_profile)
                db.flush()
            student_objs.append(stu_profile)

        # 3. COURSES (5 Courses)
        courses_data = [
            ("FS-PY-01", "Full Stack Python Web Development with FastAPI & React", "Web Development", 16, Decimal("35000.00"), "Comprehensive engineering course covering FastAPI, SQLAlchemy, React.js, Tailwind CSS, and MySQL."),
            ("CLD-DEV-02", "Enterprise Cloud DevOps & Kubernetes Infrastructure", "DevOps & Cloud", 14, Decimal("42000.00"), "Master Docker, Kubernetes, CI/CD pipelines, AWS/GCP architecture, and Terraform infrastructure."),
            ("DS-ML-03", "Applied Data Science & Machine Learning with Python", "Data Science", 16, Decimal("45000.00"), "End-to-end data science covering Pandas, NumPy, Scikit-Learn, PyTorch, and Model Deployment."),
            ("CYB-SEC-04", "Cyber Security Operations & Network Defense", "Cyber Security", 12, Decimal("38000.00"), "Ethical hacking, threat mitigation, penetration testing, and security compliance frameworks."),
            ("FE-ADV-05", "Advanced React.js & Modern UI Architecture", "Frontend Development", 10, Decimal("28000.00"), "Design systems, state management, micro-frontends, Vite, performance optimization, and testing.")
        ]
        course_objs = []
        for code, title, cat, dur, fee, desc in courses_data:
            course = db.query(Course).filter_by(code=code).first()
            if not course:
                course = Course(
                    code=code,
                    title=title,
                    category=cat,
                    duration_weeks=dur,
                    fee=fee,
                    description=desc,
                    status="published",
                    created_by_id=admin_user.id
                )
                db.add(course)
                db.flush()
            course_objs.append(course)

        # 4. MODULES & LECTURES for Course 1 & 2
        for c_idx, c in enumerate(course_objs[:3]):
            mod_titles = [
                f"Module 1: Foundations and Architecture of {c.title.split()[0]}",
                f"Module 2: Core Implementation & Business Logic in {c.title.split()[0]}",
                f"Module 3: Advanced Projects, Optimization & Deployment"
            ]
            for m_seq, m_title in enumerate(mod_titles, start=1):
                mod = db.query(CourseModule).filter_by(course_id=c.id, sequence_order=m_seq).first()
                if not mod:
                    mod = CourseModule(
                        course_id=c.id,
                        title=m_title,
                        description=f"Detailed syllabus and hands-on laboratory exercises for {m_title}.",
                        sequence_order=m_seq
                    )
                    db.add(mod)
                    db.flush()

                # Add lectures
                for l_seq in range(1, 4):
                    lec_title = f"{m_title.split(':')[1].strip()} - Session {l_seq}"
                    lec = db.query(Lecture).filter_by(module_id=mod.id, sequence_order=l_seq).first()
                    if not lec:
                        lec = Lecture(
                            module_id=mod.id,
                            title=lec_title,
                            description=f"In-depth live session covering theory, architecture, and live coding exercises for {lec_title}.",
                            sequence_order=l_seq,
                            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                            duration_minutes=90
                        )
                        db.add(lec)
                        db.flush()

                        # Add Study Material
                        mat = StudyMaterial(
                            lecture_id=lec.id,
                            title=f"Lecture Slides & Reference Notes - {lec_title}",
                            file_path="/uploads/materials/sample_lecture_notes.pdf",
                            file_type="application/pdf",
                            file_size_bytes=2450000
                        )
                        db.add(mat)
                        db.flush()

        # 5. BATCHES (5 Batches)
        batches_data = [
            ("FS-BATCH-2026-A", "Python Full Stack - Morning Batch A", course_objs[0].id, instructor_objs[0].id, date.today() - timedelta(days=45), date.today() + timedelta(days=65), "Mon, Wed, Fri", "09:00 AM - 11:00 AM", 25, "active"),
            ("FS-BATCH-2026-B", "Python Full Stack - Evening Batch B", course_objs[0].id, instructor_objs[0].id, date.today() - timedelta(days=15), date.today() + timedelta(days=95), "Tue, Thu, Sat", "06:00 PM - 08:00 PM", 30, "active"),
            ("CLD-BATCH-2026-A", "DevOps & Cloud Engineers Cohort 1", course_objs[1].id, instructor_objs[1].id, date.today() - timedelta(days=30), date.today() + timedelta(days=68), "Mon, Wed, Fri", "02:00 PM - 04:00 PM", 25, "active"),
            ("DS-BATCH-2026-A", "Data Science & AI Weekend Intensive", course_objs[2].id, instructor_objs[2].id, date.today() - timedelta(days=40), date.today() + timedelta(days=72), "Sat, Sun", "10:00 AM - 02:00 PM", 20, "active"),
            ("CYB-BATCH-2026-A", "Cyber Defense & Threat Ops Cohort", course_objs[3].id, instructor_objs[1].id, date.today() + timedelta(days=10), date.today() + timedelta(days=100), "Tue, Thu", "04:00 PM - 06:00 PM", 25, "upcoming")
        ]
        batch_objs = []
        for code, name, cid, iid, sdate, edate, days, tim, cap, bstat in batches_data:
            batch = db.query(Batch).filter_by(code=code).first()
            if not batch:
                batch = Batch(
                    code=code,
                    name=name,
                    course_id=cid,
                    instructor_id=iid,
                    start_date=sdate,
                    end_date=edate,
                    class_days=days,
                    class_timing=tim,
                    capacity=cap,
                    status=bstat
                )
                db.add(batch)
                db.flush()
            batch_objs.append(batch)

        # 6. ENROLLMENTS
        # Enroll students 0..5 in Batch 0 (Python Full Stack A)
        for s in student_objs[:6]:
            enr = db.query(Enrollment).filter_by(batch_id=batch_objs[0].id, student_id=s.id).first()
            if not enr:
                enr = Enrollment(batch_id=batch_objs[0].id, student_id=s.id, status="active")
                db.add(enr)
        # Enroll students 4..8 in Batch 2 (DevOps)
        for s in student_objs[4:9]:
            enr = db.query(Enrollment).filter_by(batch_id=batch_objs[2].id, student_id=s.id).first()
            if not enr:
                enr = Enrollment(batch_id=batch_objs[2].id, student_id=s.id, status="active")
                db.add(enr)
        # Enroll students 2..6 in Batch 3 (Data Science)
        for s in student_objs[2:7]:
            enr = db.query(Enrollment).filter_by(batch_id=batch_objs[3].id, student_id=s.id).first()
            if not enr:
                enr = Enrollment(batch_id=batch_objs[3].id, student_id=s.id, status="active")
                db.add(enr)
        db.flush()

        # 7. ASSIGNMENTS
        b0 = batch_objs[0]
        assign1 = db.query(Assignment).filter_by(batch_id=b0.id, title="FastAPI CRUD & Database Migrations Project").first()
        if not assign1:
            assign1 = Assignment(
                batch_id=b0.id,
                title="FastAPI CRUD & Database Migrations Project",
                description="Design and implement a modular REST API using FastAPI, SQLAlchemy ORM, and Alembic migrations. Follow clean architecture guidelines.",
                max_marks=100,
                due_date=datetime.utcnow() + timedelta(days=7),
                attachment_path="/uploads/assignments/assignment_1_spec.pdf",
                created_by_id=instructor_objs[0].user_id
            )
            db.add(assign1)
            db.flush()

        assign2 = db.query(Assignment).filter_by(batch_id=b0.id, title="React Frontend State Management & API Integration").first()
        if not assign2:
            assign2 = Assignment(
                batch_id=b0.id,
                title="React Frontend State Management & API Integration",
                description="Build a responsive React UI consuming the FastAPI REST endpoints. Handle loading states, form validations, and JWT token interceptors.",
                max_marks=100,
                due_date=datetime.utcnow() - timedelta(days=2),
                attachment_path="/uploads/assignments/assignment_2_spec.pdf",
                created_by_id=instructor_objs[0].user_id
            )
            db.add(assign2)
            db.flush()

        # Submissions for Assignment 2
        for s in student_objs[:4]:
            sub = db.query(Submission).filter_by(assignment_id=assign2.id, student_id=s.id).first()
            if not sub:
                sub = Submission(
                    assignment_id=assign2.id,
                    student_id=s.id,
                    file_path=f"/uploads/submissions/student_{s.id}_assign2.zip",
                    submitted_at=datetime.utcnow() - timedelta(days=3),
                    status="evaluated"
                )
                db.add(sub)
                db.flush()

                # Feedback
                fb = db.query(AssignmentFeedback).filter_by(submission_id=sub.id).first()
                if not fb:
                    fb = AssignmentFeedback(
                        submission_id=sub.id,
                        evaluated_by_id=instructor_objs[0].user_id,
                        marks_obtained=Decimal("92.00"),
                        feedback_text="Excellent work! Well-structured components, clean custom hooks, and comprehensive error handling."
                    )
                    db.add(fb)
        db.flush()

        # 8. QUIZZES
        q1 = db.query(Quiz).filter_by(batch_id=b0.id, title="FastAPI & REST Architecture Assessment").first()
        if not q1:
            q1 = Quiz(
                batch_id=b0.id,
                title="FastAPI & REST Architecture Assessment",
                description="Test your understanding of HTTP methods, dependency injection, Pydantic schemas, and SQLAlchemy sessions.",
                duration_minutes=20,
                total_marks=20,
                passing_marks=10,
                retake_allowed=True,
                max_attempts=2,
                start_time=datetime.utcnow() - timedelta(days=5),
                end_time=datetime.utcnow() + timedelta(days=15),
                is_published=True
            )
            db.add(q1)
            db.flush()

            # Questions & Options
            quiz_questions = [
                ("Which HTTP status code signifies a resource was successfully created?", 5, [
                    ("200 OK", False),
                    ("201 Created", True),
                    ("204 No Content", False),
                    ("400 Bad Request", False)
                ]),
                ("What does Pydantic primarily handle in a FastAPI application?", 5, [
                    ("Database migration execution", False),
                    ("Data validation and serialization", True),
                    ("Managing CSS styling in browser", False),
                    ("Deploying Docker containers", False)
                ]),
                ("In SQLAlchemy, what is the role of declarative_base()?", 5, [
                    ("Compiles Python code to machine bytecode", False),
                    ("Acts as the base class to maintain table catalogs and metadata", True),
                    ("Configures CORS middleware headers", False),
                    ("Hashes user passwords with bcrypt", False)
                ]),
                ("Which dependency is standard for multipart file uploads in FastAPI?", 5, [
                    ("python-multipart", True),
                    ("fastapi-uploader", False),
                    ("file-streamer-lib", False),
                    ("uvicorn-multipart", False)
                ])
            ]

            for q_text, marks, opts in quiz_questions:
                quest = Question(
                    quiz_id=q1.id,
                    question_text=q_text,
                    marks=marks
                )
                db.add(quest)
                db.flush()

                for opt_text, is_corr in opts:
                    opt = QuizOption(
                        question_id=quest.id,
                        option_text=opt_text,
                        is_correct=is_corr
                    )
                    db.add(opt)
            db.flush()

            # Add completed attempt for student 1
            stu1 = student_objs[0]
            att = db.query(QuizAttempt).filter_by(quiz_id=q1.id, student_id=stu1.id).first()
            if not att:
                att = QuizAttempt(
                    quiz_id=q1.id,
                    student_id=stu1.id,
                    started_at=datetime.utcnow() - timedelta(days=2),
                    submitted_at=datetime.utcnow() - timedelta(days=2) + timedelta(minutes=14),
                    score=Decimal("20.00"),
                    is_passed=True,
                    attempt_number=1
                )
                db.add(att)
                db.flush()

        # 9. ATTENDANCE (5 past sessions for Batch 0)
        for day_offset in range(1, 6):
            s_date = date.today() - timedelta(days=day_offset * 3)
            for stu_idx, stu in enumerate(student_objs[:6]):
                att_rec = db.query(Attendance).filter_by(batch_id=b0.id, student_id=stu.id, session_date=s_date).first()
                if not att_rec:
                    # student 1 always present, others mostly present
                    stat = "present" if (stu_idx == 0 or (stu_idx + day_offset) % 4 != 0) else "absent"
                    att_rec = Attendance(
                        batch_id=b0.id,
                        student_id=stu.id,
                        session_date=s_date,
                        status=stat,
                        marked_by_id=instructor_objs[0].user_id,
                        notes="Regular session attendance."
                    )
                    db.add(att_rec)
        db.flush()

        # 10. LECTURE PROGRESS
        first_course_lectures = db.query(Lecture).join(CourseModule).filter(CourseModule.course_id == course_objs[0].id).all()
        for lec in first_course_lectures[:6]:
            prog = db.query(LectureProgress).filter_by(student_id=student_objs[0].id, lecture_id=lec.id).first()
            if not prog:
                prog = LectureProgress(
                    student_id=student_objs[0].id,
                    lecture_id=lec.id,
                    is_completed=True,
                    completed_at=datetime.utcnow() - timedelta(days=1)
                )
                db.add(prog)
        db.flush()

        # 11. PAYMENTS & RECEIPTS
        for s_idx, s in enumerate(student_objs[:6]):
            pymt = db.query(Payment).filter_by(student_id=s.id, course_id=course_objs[0].id).first()
            if not pymt:
                is_full = (s_idx < 3)
                paid = course_objs[0].fee if is_full else Decimal("20000.00")
                pending = Decimal("0.00") if is_full else (course_objs[0].fee - paid)
                status = "paid" if is_full else "partially_paid"
                pymt = Payment(
                    student_id=s.id,
                    course_id=course_objs[0].id,
                    total_fee=course_objs[0].fee,
                    paid_amount=paid,
                    pending_amount=pending,
                    payment_date=datetime.utcnow() - timedelta(days=30 - s_idx * 2),
                    payment_method="UPI" if s_idx % 2 == 0 else "NetBanking",
                    transaction_reference=f"TXN-LMS-2026-00{s_idx + 1}",
                    status=status,
                    receipt_path=f"/uploads/receipts/receipt_TXN_00{s_idx + 1}.pdf",
                    remarks="Admission fee installment",
                    recorded_by_id=admin_user.id
                )
                db.add(pymt)
        db.flush()

        # 12. CERTIFICATES (Issue for student 1 who has cleared requirements)
        cert = db.query(Certificate).filter_by(student_id=student_objs[0].id, course_id=course_objs[0].id).first()
        if not cert:
            cert = Certificate(
                certificate_number="CERT-FS-2026-0001",
                verification_id="V-LMS-984712",
                student_id=student_objs[0].id,
                course_id=course_objs[0].id,
                issue_date=date.today(),
                pdf_path="/uploads/certificates/CERT-FS-2026-0001.pdf"
            )
            db.add(cert)
            db.flush()

        # 13. ANNOUNCEMENTS & NOTIFICATIONS
        ann1 = db.query(Announcement).filter_by(title="Welcome to the 2026 Academic Batch!").first()
        if not ann1:
            ann1 = Announcement(
                title="Welcome to the 2026 Academic Batch!",
                content="Orientation sessions for all newly admitted batches commence this Monday. Please ensure your IDE and Python/Node runtimes are configured.",
                target_role="all",
                published_by_id=admin_user.id
            )
            db.add(ann1)

        ann2 = db.query(Announcement).filter_by(title="Weekend Hackathon & Code Review").first()
        if not ann2:
            ann2 = Announcement(
                title="Weekend Hackathon & Code Review",
                content="Instructors will conduct open code review sessions this Saturday. Submit your pull requests by Friday 6 PM.",
                target_role="student",
                target_batch_id=batch_objs[0].id,
                published_by_id=instructor_objs[0].user_id
            )
            db.add(ann2)

        # Direct notifications
        notifications_data = [
            (student_objs[0].user_id, "Assignment Evaluated", "Your submission for 'React Frontend State Management' has been evaluated with score 92/100.", "success", "/student/assignments"),
            (student_objs[0].user_id, "Quiz Result Published", "You scored 20/20 in 'FastAPI & REST Architecture Assessment'. Congratulations!", "info", "/student/quizzes"),
            (instructor_objs[0].user_id, "New Assignment Submissions", "4 students have submitted 'FastAPI CRUD Project' ready for evaluation.", "warning", "/instructor/assignments"),
            (admin_user.id, "Batch Enrollment Update", "Morning Batch A has reached 24/25 capacity.", "info", "/admin/batches")
        ]
        for uid, title, msg, ntype, link in notifications_data:
            notif = db.query(Notification).filter_by(user_id=uid, title=title).first()
            if not notif:
                notif = Notification(
                    user_id=uid,
                    title=title,
                    message=msg,
                    type=ntype,
                    is_read=False,
                    link=link
                )
                db.add(notif)

        db.commit()
        print("Database successfully seeded with comprehensive synthetic data!")
        print("\nDemonstration Accounts Created:")
        print(" - Admin:      admin@lms.com / Admin@123")
        print(" - Instructor: dr.patel@lms.com / Instructor@123")
        print(" - Instructor: er.verma@lms.com / Instructor@123")
        print(" - Instructor: prof.sharma@lms.com / Instructor@123")
        print(" - Student:    student1@lms.com / Student@123 (and student2@lms.com .. student10@lms.com)")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
