# LMS Security Architecture & Implementation Specification

**Document Version:** 1.1  
**Author:** Security Engineering Team  
**Last Updated:** 2026-11-25  

---

## 1. Authentication & Token Architecture
- **Password Storage:** Industry-standard Bcrypt/Argon2 with high salt rounds (12). Plain-text passwords are never logged, persisted, or returned in any response.
- **JWT Tokens:** Signed using HMAC-SHA256 with strong entropy secret key (`JWT_SECRET`). 
- **Token Claims:** `sub` (User ID), `role` (admin | instructor | student), `email`, `exp` (configurable expiration, default 24 hours), `iat`.
- **Token Invalidation:** Token revocation / user status check verified against active database record on every protected request.

---

## 2. Authorization & Role-Based Access Control (RBAC)
- Enforced at backend dependency injection level (`require_role(["admin"])`).
- **Resource-Level Authorization:**
  - Instructors can only view/manage batches, lectures, quizzes, and attendance where `batch.instructor_id == current_user.instructor.id` (or if current_user is Admin).
  - Students can only view their own enrolled batches, submit their own assignments, attempt assigned quizzes, and view their own marks, attendance, and financial records.
  - Cross-tenant / cross-student data leaks are blocked by query filters `WHERE student_id = current_user.student.id`.

---

## 3. Data Protection & Assessment Security
- **Quiz Correct Answers Concealment:** Option queries for students explicitly omit the `is_correct` boolean. The frontend receives only option IDs and text.
- **Score Calculation Integrity:** Browser client cannot submit calculated score. Frontend submits selected option IDs; backend resolves correctness from database and computes score.
- **Timing Tampering Prevention:** Backend stores `started_at` in the database. When submission arrives, backend calculates duration elapsed.
- **File Upload Protection:** Whitelist of allowed extensions (`.pdf`, `.pptx`, `.ppt`, `.png`, `.jpg`, `.jpeg`, `.mp4`, `.zip`), MIME type checking, randomized storage filenames, and directory traversal prevention (`os.path.basename` sanitization).

---

## 4. Defense-in-Depth Checklist
| Security Control | Implementation Mechanism | Status |
|---|---|---|
| SQL Injection Prevention | SQLAlchemy Parameterized ORM Queries | Enabled |
| Cross-Site Scripting (XSS) | React automatic escaping + Pydantic string sanitization | Enabled |
| Cross-Origin Resource Sharing | FastAPI CORSMiddleware with whitelist origins | Enabled |
| Brute Force Prevention | In-memory / Redis-ready rate limiting on `/api/auth/login` | Enabled |
| Secret Exposure Prevention | Strict environment variable separation (`.env`) | Enabled |
| File Traversal Defense | UUID-based file path storage in isolated `uploads/` dir | Enabled |
