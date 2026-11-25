# LMS Technical Defense & Viva Voce Preparation Guide

**Document Version:** 1.1  
**Project:** Enterprise Role-Based Learning Management System  

---

## 1. Core Architectural Questions

### Q1: How does the application enforce Role-Based Access Control (RBAC)?
**Answer:** RBAC is enforced strictly at the backend FastAPI dependency injection layer (`require_role(["admin"])`), not merely through hidden frontend UI elements. Whenever a request arrives, the JWT Bearer token is decoded to extract `sub` and `role`. The user's active status in MySQL is verified, and their role is compared against the permitted roles for that endpoint. Any unauthorized attempt returns an HTTP 403 Forbidden.

### Q2: How is assessment integrity guaranteed in the Quiz Engine?
**Answer:**
1. **Option Secrecy:** When a student queries a quiz, the API filters out the `is_correct` field from all options. Students receive only option IDs and text.
2. **Server-Side Scoring:** The browser never sends marks. The student submits only chosen option IDs. The server validates each choice against the database and computes the score.
3. **Timer Security:** Backend timestamps (`started_at` and `submitted_at`) are verified against `duration_minutes` to prevent client clock manipulation.

### Q3: What is the formula for calculating Student Course Progress?
**Answer:**
$$\text{Overall Progress} = (0.40 \times \text{Lecture Completion \%}) + (0.30 \times \text{Assignment Completion \%}) + (0.30 \times \text{Quiz Completion \%})$$
- Lecture completion tracks verified `lecture_progress` rows.
- Assignment completion calculates evaluated submissions over batch assignments.
- Quiz completion tracks passed quizzes over published batch quizzes.

### Q4: How is duplicate prevention handled across academic entities?
**Answer:**
- Batches enforce a unique composite constraint `uq_batch_student (batch_id, student_id)`.
- Attendance enforces `uq_attendance_session (batch_id, student_id, session_date)`.
- Assignment submissions enforce `uq_assignment_student (assignment_id, student_id)`.
- Certificate issuance enforces unique `certificate_number` and `verification_id`.

### Q5: How does PDF generation function for certificates and receipts?
**Answer:** The backend uses the Python `reportlab` library inside a dedicated `pdf_service.py`. When a student clears eligibility criteria or an admin records a tuition payment, the service draws official typography, canvas graphics, and unique verification hashes, saving the PDF to persistent storage and returning the downloadable URL.
