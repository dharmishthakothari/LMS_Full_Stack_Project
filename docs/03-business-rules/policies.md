# LMS Business Rules & Policy Document

**Document Version:** 1.1  
**Author:** Software Architecture Team  
**Last Updated:** 2026-11-25  

---

## 1. Academic & Enrollment Policies

### 1.1 Batch Capacity Enforcement
- Each batch defines a maximum capacity `capacity >= 1`.
- An enrollment transaction must fail with HTTP 400 if `current_enrolled_count >= capacity`.
- Duplicate enrollment of a student in the same batch is strictly prevented by a unique constraint on `(batch_id, student_id)`.

### 1.2 Course Deletion & Archival Policy
- Hard deletion of a course is disallowed if active batches or student enrollments exist.
- Instead, the course status transitions to `archived` or `unpublished`.

---

## 2. Assessment & Grading Policies

### 2.1 Assignment Submissions & Deadlines
- Submissions received after the configured `due_date` are marked with status `late_submission`.
- Maximum marks must be a positive integer.
- Graded marks cannot exceed the assignment's `max_marks`.

### 2.2 Quiz Engine Integrity Rules
- Correct answer flags (`is_correct`) must NEVER be transmitted to the client before or during an active quiz attempt.
- Quiz duration is strictly enforced using server-side timestamps: `elapsed_seconds = now() - attempt.start_time`.
- If `elapsed_seconds > (quiz.duration_minutes * 60 + grace_period_seconds)`, the submission is flagged as auto-submitted or rejected.
- Marks and pass/fail calculations are executed strictly on the backend.
- Retakes are prohibited unless `quiz.retake_allowed == True` and `attempt_count < quiz.max_attempts`.

---

## 3. Attendance Calculation Policy
$$\text{Attendance Percentage} = \left(\frac{\text{Total Present Sessions}}{\text{Total Sessions Recorded}}\right) \times 100$$
- Only instructors assigned to the batch or system administrators can log or modify attendance.
- Attendance updates create an audit log entry.
- Unique constraint enforces at most one record per `(batch_id, student_id, session_date)`.

---

## 4. Student Progress Formula
The overall course progress percentage is computed dynamically as a weighted aggregate:
$$\text{Progress \%} = (0.40 \times \text{Lecture Completion \%}) + (0.30 \times \text{Assignment Completion \%}) + (0.30 \times \text{Quiz Completion \%})$$
- **Lecture Completion %** = $(\text{Completed Lectures} / \text{Total Published Lectures}) \times 100$
- **Assignment Completion %** = $(\text{Evaluated Assignments} / \text{Total Batch Assignments}) \times 100$
- **Quiz Completion %** = $(\text{Passed Quizzes} / \text{Total Batch Quizzes}) \times 100$

---

## 5. Certificate Issuance Eligibility Policy
A student is eligible for an automated, verified completion certificate if and only if:
1. `Course Progress Percentage >= 80%`
2. `Attendance Percentage >= 75%`
3. `Pending Course Fee == 0` (All dues cleared)

Duplicate certificates for the same student and course cannot be generated.

---

## 6. Financial Ledger & Fee Payment Policy
- System supports multi-installment partial payments.
- `Pending Amount = Course Fee - Total Approved Payments`.
- Negative payment amounts or payments exceeding the pending balance are rejected.
- Every payment generates an official payment receipt with a unique receipt reference number.
