# Architecture & Module Prompts Log

This document archives the structured prompt templates and engineering guidelines utilized to construct the full stack LMS application modules.

---

## 1. Authentication & Security Prompt
```text
Act as Senior Python Security Architect. Design a production-grade authentication module for FastAPI:
- Implement password hashing with Passlib and Bcrypt.
- Issue JWT tokens using PyJWT / python-jose with HS256.
- Enforce strict RBAC dependencies: get_current_user, require_role(["admin", "instructor", "student"]).
- Include forgot password and reset password token mechanisms.
- Add rate limiting and prevent timing attacks on credential validation.
```

---

## 2. Course & Curriculum Management Prompt
```text
Act as Database Architect and FastAPI Engineer. Design the Course and Batch hierarchy:
- A Course contains sequential CourseModules.
- A Batch belongs to a Course, is assigned an Instructor, and enrolls Students via an Enrollment association table.
- Enforce batch capacity constraints.
- Provide full CRUD operations with comprehensive Pydantic v2 schemas and validation.
```

---

## 3. Assessment & Examination Engine Prompt
```text
Design an Assessment & Quiz Engine adhering to academic integrity standards:
- Support MCQs with configurable timer limits and passing criteria.
- Conceal 'is_correct' flags when students initiate an attempt to prevent client-side inspection.
- Score attempts server-side upon submission and record detailed question-level answers.
- Implement weighted progress calculation combining lectures, assignments, and quizzes.
```

---

## 4. PDF Generation & Reporting Engine Prompt
```text
Implement production ReportLab PDF generators:
- Course Completion Certificate with border styling, verification QR code, and signatures.
- Official Fee Receipt with tabular fee breakdown and tax calculations.
- Multi-format report exporter supporting CSV, Excel (openpyxl), and PDF.
- Expose public certificate verification API without authentication requirements.
```
