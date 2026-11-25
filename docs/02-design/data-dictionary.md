# LMS Complete Database Data Dictionary

**Document Version:** 1.1  
**Author:** Database Architecture Team  
**Last Updated:** 2026-11-25  

---

## 1. Entity Catalog (24 Primary Tables)

### Table 1: `roles`
Stores standard user roles.
- `id`: INT, Primary Key, Auto Increment
- `name`: VARCHAR(50), Unique, Not Null ('admin', 'instructor', 'student')
- `description`: VARCHAR(255), Nullable
- `created_at`: DATETIME, Default UTC

### Table 2: `users`
Core user identity and authentication credentials.
- `id`: INT, Primary Key, Auto Increment
- `role_id`: INT, Foreign Key -> `roles(id)` ON DELETE RESTRICT
- `email`: VARCHAR(255), Unique, Indexed, Not Null
- `password_hash`: VARCHAR(255), Not Null
- `first_name`: VARCHAR(100), Not Null
- `last_name`: VARCHAR(100), Not Null
- `phone`: VARCHAR(20), Nullable
- `profile_image`: VARCHAR(500), Nullable
- `is_active`: BOOLEAN, Default TRUE, Indexed
- `created_at`: DATETIME, Default UTC
- `updated_at`: DATETIME, Default UTC, ON UPDATE UTC

### Table 3: `instructors`
Profile details specific to faculty.
- `id`: INT, Primary Key, Auto Increment
- `user_id`: INT, Foreign Key -> `users(id)` ON DELETE CASCADE, Unique
- `expertise`: VARCHAR(255), Nullable
- `qualification`: VARCHAR(255), Nullable
- `biography`: TEXT, Nullable

### Table 4: `students`
Profile details specific to enrolled learners.
- `id`: INT, Primary Key, Auto Increment
- `user_id`: INT, Foreign Key -> `users(id)` ON DELETE CASCADE, Unique
- `date_of_birth`: DATE, Nullable
- `address`: TEXT, Nullable
- `emergency_contact`: VARCHAR(50), Nullable
- `joining_date`: DATE, Default CURRENT_DATE

### Table 5: `courses`
Curriculum catalog.
- `id`: INT, Primary Key, Auto Increment
- `title`: VARCHAR(255), Not Null, Indexed
- `code`: VARCHAR(50), Unique, Not Null
- `category`: VARCHAR(100), Not Null, Indexed
- `description`: TEXT, Nullable
- `duration_weeks`: INT, Not Null, Default 12
- `fee`: DECIMAL(10, 2), Not Null, Default 0.00
- `thumbnail_url`: VARCHAR(500), Nullable
- `status`: ENUM('draft', 'published', 'unpublished', 'archived'), Default 'draft', Indexed
- `created_by_id`: INT, Foreign Key -> `users(id)`
- `created_at`: DATETIME, Default UTC
- `updated_at`: DATETIME, Default UTC

### Table 6: `course_modules`
Structured chapters/sections under a course.
- `id`: INT, Primary Key, Auto Increment
- `course_id`: INT, Foreign Key -> `courses(id)` ON DELETE CASCADE
- `title`: VARCHAR(255), Not Null
- `description`: TEXT, Nullable
- `sequence_order`: INT, Not Null, Default 1
- `created_at`: DATETIME, Default UTC

### Table 7: `batches`
Operational cohorts for teaching and scheduling.
- `id`: INT, Primary Key, Auto Increment
- `name`: VARCHAR(150), Not Null
- `code`: VARCHAR(50), Unique, Not Null
- `course_id`: INT, Foreign Key -> `courses(id)` ON DELETE RESTRICT
- `instructor_id`: INT, Foreign Key -> `instructors(id)` ON DELETE SET NULL
- `start_date`: DATE, Not Null
- `end_date`: DATE, Not Null
- `class_days`: VARCHAR(100), Not Null (e.g., 'Mon, Wed, Fri')
- `class_timing`: VARCHAR(100), Not Null (e.g., '10:00 AM - 12:00 PM')
- `capacity`: INT, Not Null, Default 30
- `status`: ENUM('upcoming', 'active', 'completed', 'closed', 'archived'), Default 'upcoming', Indexed
- `created_at`: DATETIME, Default UTC

### Table 8: `enrollments` / `batch_students`
Mapping of students to batches and enrollment statuses.
- `id`: INT, Primary Key, Auto Increment
- `batch_id`: INT, Foreign Key -> `batches(id)` ON DELETE CASCADE
- `student_id`: INT, Foreign Key -> `students(id)` ON DELETE CASCADE
- `enrolled_at`: DATETIME, Default UTC
- `status`: ENUM('active', 'completed', 'dropped'), Default 'active'
- UNIQUE CONSTRAINT `uq_batch_student`: (`batch_id`, `student_id`)

### Table 9: `lectures`
Individual class sessions and syllabus milestones.
- `id`: INT, Primary Key, Auto Increment
- `module_id`: INT, Foreign Key -> `course_modules(id)` ON DELETE CASCADE
- `batch_id`: INT, Foreign Key -> `batches(id)` ON DELETE CASCADE, Nullable
- `title`: VARCHAR(255), Not Null
- `description`: TEXT, Nullable
- `sequence_order`: INT, Not Null, Default 1
- `video_url`: VARCHAR(500), Nullable
- `duration_minutes`: INT, Default 60
- `created_at`: DATETIME, Default UTC

### Table 10: `study_materials`
Downloadable assets (PDFs, PPTs, code archives).
- `id`: INT, Primary Key, Auto Increment
- `lecture_id`: INT, Foreign Key -> `lectures(id)` ON DELETE CASCADE
- `title`: VARCHAR(255), Not Null
- `file_path`: VARCHAR(500), Not Null
- `file_type`: VARCHAR(50), Not Null
- `file_size_bytes`: BIGINT, Not Null
- `created_at`: DATETIME, Default UTC

### Table 11: `assignments`
Tasks given to a batch with grading parameters.
- `id`: INT, Primary Key, Auto Increment
- `batch_id`: INT, Foreign Key -> `batches(id)` ON DELETE CASCADE
- `title`: VARCHAR(255), Not Null
- `description`: TEXT, Not Null
- `max_marks`: INT, Not Null, Default 100
- `due_date`: DATETIME, Not Null
- `attachment_path`: VARCHAR(500), Nullable
- `created_by_id`: INT, Foreign Key -> `users(id)`
- `created_at`: DATETIME, Default UTC

### Table 12: `submissions`
Student assignment deliverables.
- `id`: INT, Primary Key, Auto Increment
- `assignment_id`: INT, Foreign Key -> `assignments(id)` ON DELETE CASCADE
- `student_id`: INT, Foreign Key -> `students(id)` ON DELETE CASCADE
- `file_path`: VARCHAR(500), Not Null
- `submitted_at`: DATETIME, Default UTC
- `status`: ENUM('submitted', 'under_review', 'evaluated', 'late_submission'), Default 'submitted'
- UNIQUE CONSTRAINT: (`assignment_id`, `student_id`)

### Table 13: `assignment_feedback`
Instructor grading and critique.
- `id`: INT, Primary Key, Auto Increment
- `submission_id`: INT, Foreign Key -> `submissions(id)` ON DELETE CASCADE, Unique
- `evaluated_by_id`: INT, Foreign Key -> `users(id)`
- `marks_obtained`: DECIMAL(5, 2), Not Null
- `feedback_text`: TEXT, Nullable
- `evaluated_at`: DATETIME, Default UTC

### Table 14: `quizzes`
MCQ examination containers.
- `id`: INT, Primary Key, Auto Increment
- `batch_id`: INT, Foreign Key -> `batches(id)` ON DELETE CASCADE
- `title`: VARCHAR(255), Not Null
- `description`: TEXT, Nullable
- `duration_minutes`: INT, Not Null, Default 30
- `total_marks`: INT, Not Null, Default 100
- `passing_marks`: INT, Not Null, Default 40
- `retake_allowed`: BOOLEAN, Default FALSE
- `max_attempts`: INT, Default 1
- `start_time`: DATETIME, Nullable
- `end_time`: DATETIME, Nullable
- `is_published`: BOOLEAN, Default FALSE
- `created_at`: DATETIME, Default UTC

### Table 15: `questions`
Questions within a quiz.
- `id`: INT, Primary Key, Auto Increment
- `quiz_id`: INT, Foreign Key -> `quizzes(id)` ON DELETE CASCADE
- `question_text`: TEXT, Not Null
- `marks`: INT, Not Null, Default 1
- `sequence_order`: INT, Default 1

### Table 16: `quiz_options`
Multiple-choice options for a question.
- `id`: INT, Primary Key, Auto Increment
- `question_id`: INT, Foreign Key -> `questions(id)` ON DELETE CASCADE
- `option_text`: TEXT, Not Null
- `is_correct`: BOOLEAN, Not Null, Default FALSE

### Table 17: `quiz_attempts`
Student test attempts.
- `id`: INT, Primary Key, Auto Increment
- `quiz_id`: INT, Foreign Key -> `quizzes(id)` ON DELETE CASCADE
- `student_id`: INT, Foreign Key -> `students(id)` ON DELETE CASCADE
- `started_at`: DATETIME, Default UTC
- `submitted_at`: DATETIME, Nullable
- `score`: DECIMAL(5, 2), Default 0.00
- `is_passed`: BOOLEAN, Default FALSE
- `attempt_number`: INT, Default 1

### Table 18: `quiz_answers`
Individual answers recorded per attempt.
- `id`: INT, Primary Key, Auto Increment
- `attempt_id`: INT, Foreign Key -> `quiz_attempts(id)` ON DELETE CASCADE
- `question_id`: INT, Foreign Key -> `questions(id)` ON DELETE CASCADE
- `selected_option_id`: INT, Foreign Key -> `quiz_options(id)` ON DELETE CASCADE, Nullable
- `is_correct`: BOOLEAN, Default FALSE

### Table 19: `attendance`
Attendance record per student per batch session.
- `id`: INT, Primary Key, Auto Increment
- `batch_id`: INT, Foreign Key -> `batches(id)` ON DELETE CASCADE
- `student_id`: INT, Foreign Key -> `students(id)` ON DELETE CASCADE
- `session_date`: DATE, Not Null
- `status`: ENUM('present', 'absent', 'late', 'excused'), Default 'present'
- `marked_by_id`: INT, Foreign Key -> `users(id)`
- `notes`: VARCHAR(255), Nullable
- `created_at`: DATETIME, Default UTC
- UNIQUE CONSTRAINT: (`batch_id`, `student_id`, `session_date`)

### Table 20: `lecture_progress`
Tracks student completion of specific lectures.
- `id`: INT, Primary Key, Auto Increment
- `student_id`: INT, Foreign Key -> `students(id)` ON DELETE CASCADE
- `lecture_id`: INT, Foreign Key -> `lectures(id)` ON DELETE CASCADE
- `is_completed`: BOOLEAN, Default TRUE
- `completed_at`: DATETIME, Default UTC
- UNIQUE CONSTRAINT: (`student_id`, `lecture_id`)

### Table 21: `certificates`
Official completion credentials.
- `id`: INT, Primary Key, Auto Increment
- `certificate_number`: VARCHAR(100), Unique, Not Null
- `verification_id`: VARCHAR(100), Unique, Not Null, Indexed
- `student_id`: INT, Foreign Key -> `students(id)` ON DELETE CASCADE
- `course_id`: INT, Foreign Key -> `courses(id)` ON DELETE RESTRICT
- `issue_date`: DATE, Not Null
- `pdf_path`: VARCHAR(500), Not Null
- `created_at`: DATETIME, Default UTC

### Table 22: `payments`
Financial ledger records for course fees.
- `id`: INT, Primary Key, Auto Increment
- `student_id`: INT, Foreign Key -> `students(id)` ON DELETE CASCADE
- `course_id`: INT, Foreign Key -> `courses(id)` ON DELETE RESTRICT
- `total_fee`: DECIMAL(10, 2), Not Null
- `paid_amount`: DECIMAL(10, 2), Not Null
- `pending_amount`: DECIMAL(10, 2), Not Null
- `payment_date`: DATETIME, Default UTC
- `payment_method`: VARCHAR(50), Not Null (e.g., 'UPI', 'NetBanking', 'Card', 'Cash')
- `transaction_reference`: VARCHAR(100), Unique, Not Null
- `status`: ENUM('paid', 'partially_paid', 'pending', 'failed', 'refunded'), Default 'paid'
- `receipt_path`: VARCHAR(500), Nullable
- `remarks`: VARCHAR(255), Nullable
- `recorded_by_id`: INT, Foreign Key -> `users(id)`

### Table 23: `notifications`
Direct in-app alerts sent to specific users.
- `id`: INT, Primary Key, Auto Increment
- `user_id`: INT, Foreign Key -> `users(id)` ON DELETE CASCADE
- `title`: VARCHAR(200), Not Null
- `message`: TEXT, Not Null
- `type`: VARCHAR(50), Default 'info'
- `is_read`: BOOLEAN, Default FALSE, Indexed
- `link`: VARCHAR(255), Nullable
- `created_at`: DATETIME, Default UTC

### Table 24: `announcements`
Broadcast messages to roles or batches.
- `id`: INT, Primary Key, Auto Increment
- `title`: VARCHAR(255), Not Null
- `content`: TEXT, Not Null
- `target_role`: VARCHAR(50), Nullable ('all', 'admin', 'instructor', 'student')
- `target_batch_id`: INT, Foreign Key -> `batches(id)` ON DELETE SET NULL, Nullable
- `published_by_id`: INT, Foreign Key -> `users(id)`
- `created_at`: DATETIME, Default UTC
