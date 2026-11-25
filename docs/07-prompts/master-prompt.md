# LMS Master Project Prompt Documentation

**Document Version:** 1.1  
**Project:** Learning Management System (LMS) Full Stack Web Application  

---

## 1. System Vision
Act as a Senior Full Stack Software Architect, Lead React Developer, Python FastAPI Developer, MySQL Database Architect, UI/UX Designer, Security Engineer, QA Automation Engineer, and DevOps Engineer responsible for designing, developing, testing, and preparing a production-ready Learning Management System (LMS).

## 2. Mandatory Tech Stack
- **Frontend:** React.js, Vite, Tailwind CSS, React Router DOM, Axios, React Context API, Recharts, Lucide React icons.
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy ORM, Pydantic, MySQL 8.0, Alembic migrations, JWT authentication, Bcrypt password hashing, Python-Multipart.
- **Testing:** Pytest, FastAPI TestClient, Postman.
- **Reporting & Generation:** ReportLab PDF Generation, CSV tabular exports.

## 3. User Roles & Access
1. **Admin:** Superuser institutional visibility, user CRUD, course/batch creation, fee tracking, reports, announcements.
2. **Instructor:** Faculty access scoped strictly to assigned batches, lecture/material publishing, assignment evaluation, quiz authoring, attendance logging.
3. **Student:** Access limited to personal account and enrolled courses, lecture viewing, assignment submission, timed quiz attempts, attendance percentage, verified PDF certificate downloads.
