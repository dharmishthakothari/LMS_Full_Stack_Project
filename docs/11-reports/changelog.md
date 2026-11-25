# LMS Project Changelog & Version History

**Current Version:** 1.1.0  

---

### [1.1.0] - 2026-11-25
#### Added
- Complete SQLAlchemy Declarative Schema for all 24 relational tables with indexes and foreign key constraints.
- Alembic database migration environment and initial baseline revision.
- Comprehensive synthetic seed dataset creating 1 Admin, 3 Faculty Instructors, 10 Enrolled Students, 5 Courses, 5 Batches, Lectures, Assignments, Submissions, Quizzes, Attendance records, and Payments.
- 51 REST API endpoints covering Authentication, User Management, Courses, Modules, Batches, Lectures, Assignments, Quizzes, Attendance, Progress, Certificates, Payments, Communications, and Analytics.
- Automated ReportLab PDF generator for official Payment Receipts and Course Completion Certificates.
- Server-side scoring engine with live countdown timer and anti-tamper answer concealment.
- Automated Pytest test suite with 16 comprehensive integration and RBAC test cases (100% passing).
- Modern SaaS React SPA built with Vite, Tailwind CSS, Lucide Icons, and Recharts charts.
- Public certificate verification tool validating unique cryptographic verification codes against MySQL.
- Full 22-document system specifications under `/docs`, including 15 per-module guides (`docs/06-modules/`), UI wireframes (`docs/02-design/wireframes/wireframes.md`), and demo script (`docs/11-reports/demo-script.md`).
- Password recovery (`ForgotPassword.jsx`, `ResetPassword.jsx`) and dedicated `NotificationsPage.jsx` frontend views.
- Cloud deployment configurations (`frontend/netlify.toml`, `frontend/vercel.json`, `render.yaml`, `backend/Procfile`) and live Netlify frontend deployment (`https://lms-fullstack-platform.netlify.app`).

#### Changed
- Migrated all 25 Pydantic schema `Config` classes to Pydantic v2 `ConfigDict(from_attributes=True)`, eliminating deprecation warnings across all 16 Pytest tests.
- Replaced synthetic enrollment trends in `/api/reports/dashboard` with dynamic, database-aggregated monthly enrollment queries via SQLAlchemy `func.extract`.
- Enhanced quiz scheduling security in `/api/quizzes/{id}/start` with strict UTC time window enforcement (`start_time` / `end_time`).
- Added convenience and aggregation endpoints: `GET /api/progress/me` and `GET /api/payments/student/{id}/summary`.
- Added Notifications navigation item directly into the responsive sidebar for all user roles.
- Enhanced Mermaid ERD in `docs/04-architecture/architecture.md` with full 24-entity visual schema.
