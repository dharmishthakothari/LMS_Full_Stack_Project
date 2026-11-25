# LMS Use Cases & User Stories

**Document Version:** 1.1  
**Author:** Software Architecture Team  
**Last Updated:** 2026-11-25  

---

## 1. Actor Catalog
- **ACT-01 Admin:** Superuser with full system access across all tenants, users, batches, courses, and financial records.
- **ACT-02 Instructor:** Faculty member with permissions scoped to assigned batches and courses.
- **ACT-03 Student:** Enrolled learner with read/write access limited to personal records, assigned batch materials, assignments, and quizzes.

---

## 2. Key Use Cases

### UC-01: User Authentication & Profile Lifecycle
- **Actors:** All
- **Preconditions:** User account exists and status is 'active'.
- **Main Flow:**
  1. User submits email and password.
  2. System validates credentials using Bcrypt/Argon2.
  3. System issues signed JWT token containing `user_id`, `email`, and `role`.
  4. Client stores token securely and accesses role-appropriate dashboard.
- **Exceptions:** Inactive account returns 403 Forbidden; invalid credentials return generic 401 Unauthorized.

### UC-02: Course & Module Structuring
- **Actors:** Admin
- **Main Flow:**
  1. Admin creates Course (Title, Description, Category, Duration, Fee, Thumbnail).
  2. Admin defines sequential Course Modules.
  3. Admin publishes course to make it available for batch creation and enrollment.

### UC-03: Batch Scheduling & Student Roster
- **Actors:** Admin
- **Main Flow:**
  1. Admin creates a Batch linked to a Course with Start Date, End Date, Schedule, and Capacity.
  2. Admin assigns an Instructor to the Batch.
  3. Admin enrolls Students into the Batch, validating that enrollment does not exceed batch capacity and no duplicate enrollment occurs.

### UC-04: Lecture & Content Delivery
- **Actors:** Instructor, Student
- **Main Flow:**
  1. Instructor uploads lecture notes (PDF/PPT) or links video resources to a specific module.
  2. Enrolled students view lectures and download materials.
  3. Student marks lecture as completed; backend records `lecture_progress` and recalculates overall course progress.

### UC-05: Assignment Submission & Evaluation
- **Actors:** Instructor, Student
- **Main Flow:**
  1. Instructor creates assignment with deadline, maximum marks, and reference attachments.
  2. Student submits assignment file before deadline (or flagged as late submission).
  3. Instructor evaluates submission, inputs marks and qualitative feedback.
  4. Student receives evaluation notification and views graded feedback.

### UC-06: Timed MCQ Quiz Examination
- **Actors:** Instructor, Student
- **Main Flow:**
  1. Instructor authors Quiz with MCQ questions, choices, passing score, duration, and window.
  2. Student begins Quiz; server creates `quiz_attempt` with start timestamp.
  3. Client displays countdown timer; student submits answers.
  4. Server calculates score strictly on backend against correct options; saves attempt result.
  5. Student views score and allowed review. Correct answers are never sent to frontend prior to submission.

### UC-07: Attendance Recording & Audit
- **Actors:** Instructor, Admin, Student
- **Main Flow:**
  1. Instructor opens batch roster for a session date and marks each student Present or Absent.
  2. Backend ensures no duplicate record exists for student + batch + date.
  3. Student views personal attendance percentage: `(Present Sessions / Total Sessions) * 100`.

### UC-08: Certificate Generation & Verification
- **Actors:** Student, Admin, Public Verifier
- **Main Flow:**
  1. System checks student eligibility: Course progress >= 80%, Attendance >= 75%, and Fees fully cleared.
  2. If eligible, student or admin triggers Certificate Generation.
  3. Server generates high-resolution PDF certificate with unique Verification Code.
  4. External parties can verify authenticity via `/api/certificates/verify/{verification_id}`.

### UC-09: Fee Tracking & PDF Receipts
- **Actors:** Admin, Student
- **Main Flow:**
  1. Admin records course payment (Full or Partial installment) with transaction reference.
  2. Backend computes updated pending balance: `Total Fee - Total Paid`.
  3. Admin or Student downloads generated official PDF Payment Receipt.
