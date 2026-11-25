# LMS Test Plan & Automated Verification Matrix

**Document Version:** 1.1  
**Author:** QA Automation Team  
**Last Updated:** 2026-11-25  

---

## 1. Test Strategy & Objectives
The primary objective of automated testing is to verify strict role-based access control (RBAC), database relationship constraints, integrity of financial ledgers, score computation secrecy, and end-to-end API workflows.

## 2. Test Execution Environment
- **Framework:** Pytest 9.2 + FastAPI TestClient + Starlette HTTPX
- **Database Engine:** MySQL 8.0 on `localhost:3306` (`lms_db`)
- **Backend Runtime:** Python 3.11.9
- **Frontend Compiler:** Vite 8.3 + React 19 + Tailwind CSS

## 3. Test Suites Catalog
1. `test_auth.py`: Verifies credential validation, Bcrypt password checking, inactive user login blocking, profile retrieval, and health check connectivity.
2. `test_rbac.py`: Validates role guards. Tests that students cannot access `/api/users` (403 Forbidden), instructors cannot create users (403), and students cannot post payments (403).
3. `test_courses_batches.py`: Validates course creation, batch scheduling constraints (end date cannot precede start date), capacity enforcement, and enrollment idempotency.
4. `test_assessments.py`: Verifies assignment creation, submission file upload, marks validation (marks > max marks rejected), MCQ quiz question secrecy (correct answers omitted for students), and public certificate verification.
