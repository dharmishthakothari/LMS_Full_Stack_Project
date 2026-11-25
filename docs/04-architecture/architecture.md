# LMS Technical Architecture & System Design

**Document Version:** 1.1  
**Author:** Full Stack Architecture Team  
**Last Updated:** 2026-11-25  

---

## 1. Architectural Overview

The application follows a clean 3-tier decoupled architecture:
1. **Frontend Presentation Tier:** Single Page Application (SPA) built with React 18, Vite, Tailwind CSS, Lucide Icons, and Recharts.
2. **Backend Application Tier:** Asynchronous REST API service built with Python 3.11+ and FastAPI, utilizing Pydantic v2 for data validation and SQLAlchemy 2.0 ORM.
3. **Database & Storage Tier:** MySQL 8.0 relational database with connection pooling, and local/S3-compatible object storage abstraction for documents, lecture media, and generated PDF receipts/certificates.

```mermaid
graph TD
    Client["Client Browser (React 18 + Tailwind CSS + Recharts)"]
    API["FastAPI REST API Server (Python 3.11)"]
    Auth["JWT RBAC Security Middleware"]
    Services["Business Service Layer"]
    ORM["SQLAlchemy 2.0 ORM"]
    DB[("MySQL 8.0 Relational DB")]
    Storage["Object Storage / File Service"]
    PDF["ReportLab PDF Generation Service"]

    Client -->|HTTPS / JSON / Bearer JWT| API
    API --> Auth
    Auth --> Services
    Services --> ORM
    Services --> Storage
    Services --> PDF
    ORM --> DB
```

---

## 2. Directory Layout & Separation of Concerns

```
LMS_Application_With_Vibe/
├── backend/
│   ├── app/
│   │   ├── main.py              # Application entry point, CORS, exception handlers
│   │   ├── config.py            # Pydantic BaseSettings environment configuration
│   │   ├── database.py          # SQLAlchemy engine, session maker, base model
│   │   ├── models/              # Declarative SQLAlchemy models (24+ entities)
│   │   ├── schemas/             # Pydantic request/response validation schemas
│   │   ├── routers/             # API route controllers grouped by domain
│   │   ├── services/            # Pure business logic and calculation services
│   │   ├── dependencies/        # FastApi auth, RBAC, DB session dependencies
│   │   ├── middleware/          # Security headers, rate limiting, request logging
│   │   └── utils/               # PDF generation, file handlers, security helpers
│   ├── migrations/              # Alembic environment and migration scripts
│   ├── tests/                   # Pytest automated test suites
│   ├── uploads/                 # Storage for files, receipts, certificates
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── assets/              # Static icons, logos, brand styling
│   │   ├── components/          # Reusable UI widgets (Tables, Modals, StatCards)
│   │   ├── context/             # AuthContext, NotificationContext, ThemeContext
│   │   ├── hooks/               # Custom React hooks (useAuth, useFetch)
│   │   ├── layouts/             # AdminLayout, InstructorLayout, StudentLayout
│   │   ├── pages/               # 42 functional screen views across roles
│   │   ├── routes/              # Protected routes & RoleGuard components
│   │   ├── services/            # Axios API client modules
│   │   └── utils/               # Formatting, date helpers, validation rules
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
└── docs/                        # Complete 22-document system specifications
```

---

## 3. Database Entity Relationship Overview

![LMS Relational Database Architecture ERD](erd.png)

The core schema comprises 24 relational tables organized into clear functional domains: Identity & Access, Academic Catalog, Batches & Delivery, Assessments & Grading, Student Engagement & Tracking, and Communications & Finance.

```mermaid
erDiagram
    ROLES ||--o{ USERS : assigns
    USERS ||--o| INSTRUCTORS : profiles
    USERS ||--o| STUDENTS : profiles
    USERS ||--o{ NOTIFICATIONS : receives
    USERS ||--o{ ANNOUNCEMENTS : publishes

    COURSES ||--o{ COURSE_MODULES : contains
    COURSES ||--o{ BATCHES : offers
    COURSES ||--o{ PAYMENTS : charges
    COURSES ||--o{ CERTIFICATES : grants

    COURSE_MODULES ||--o{ LECTURES : includes
    LECTURES ||--o{ STUDY_MATERIALS : provides
    LECTURES ||--o{ LECTURE_PROGRESS : tracks

    INSTRUCTORS ||--o{ BATCHES : leads
    BATCHES ||--o{ ENROLLMENTS : registers
    STUDENTS ||--o{ ENROLLMENTS : joins

    BATCHES ||--o{ ASSIGNMENTS : assigns
    ASSIGNMENTS ||--o{ SUBMISSIONS : receives
    SUBMISSIONS ||--o{ ASSIGNMENT_FEEDBACK : evaluates

    BATCHES ||--o{ QUIZZES : schedules
    QUIZZES ||--o{ QUESTIONS : contains
    QUESTIONS ||--o{ QUIZ_OPTIONS : offers
    QUIZZES ||--o{ QUIZ_ATTEMPTS : logs
    STUDENTS ||--o{ QUIZ_ATTEMPTS : takes
    QUIZ_ATTEMPTS ||--o{ QUIZ_ANSWERS : records
    QUESTIONS ||--o{ QUIZ_ANSWERS : answers

    BATCHES ||--o{ ATTENDANCE : marks
    STUDENTS ||--o{ ATTENDANCE : attends

    STUDENTS ||--o{ LECTURE_PROGRESS : completes
    STUDENTS ||--o{ CERTIFICATES : earns
    STUDENTS ||--o{ PAYMENTS : pays
    BATCHES ||--o{ ANNOUNCEMENTS : targets

    ROLES {
        int id PK
        string name
        string description
    }
    USERS {
        int id PK
        string email UK
        string hashed_password
        string first_name
        string last_name
        int role_id FK
        boolean is_active
    }
    INSTRUCTORS {
        int id PK
        int user_id FK,UK
        string employee_code UK
        string designation
        string department
    }
    STUDENTS {
        int id PK
        int user_id FK,UK
        string enrollment_number UK
        date date_of_birth
        date joining_date
    }
    COURSES {
        int id PK
        string code UK
        string title
        decimal fee
        string status
    }
    COURSE_MODULES {
        int id PK
        int course_id FK
        string title
        int sequence_order
    }
    LECTURES {
        int id PK
        int module_id FK
        string title
        int duration_minutes
        string video_url
    }
    BATCHES {
        int id PK
        int course_id FK
        int instructor_id FK
        string name
        int capacity
        string status
    }
    ENROLLMENTS {
        int id PK
        int student_id FK
        int batch_id FK
        datetime enrolled_at
        string status
    }
    ASSIGNMENTS {
        int id PK
        int batch_id FK
        string title
        datetime due_date
        int max_score
    }
    SUBMISSIONS {
        int id PK
        int assignment_id FK
        int student_id FK
        datetime submitted_at
        string status
        decimal score
    }
    QUIZZES {
        int id PK
        int batch_id FK
        string title
        int duration_minutes
        int passing_marks
        boolean is_published
    }
    QUESTIONS {
        int id PK
        int quiz_id FK
        string question_text
        int marks
    }
    QUIZ_OPTIONS {
        int id PK
        int question_id FK
        string option_text
        boolean is_correct
    }
    QUIZ_ATTEMPTS {
        int id PK
        int quiz_id FK
        int student_id FK
        decimal score
        boolean is_passed
    }
    ATTENDANCE {
        int id PK
        int batch_id FK
        int student_id FK
        date session_date
        string status
    }
    CERTIFICATES {
        int id PK
        int student_id FK
        int course_id FK
        string certificate_number UK
        string verification_hash UK
    }
    PAYMENTS {
        int id PK
        int student_id FK
        int course_id FK
        decimal total_fee
        decimal paid_amount
        decimal pending_amount
        string status
    }
```

The core entities form a comprehensive academic graph:
- `users` (1) <---> (1) `roles`
- `users` (1) <---> (0..1) `instructors`
- `users` (1) <---> (0..1) `students`
- `courses` (1) <---> (M) `course_modules`
- `course_modules` (1) <---> (M) `lectures`
- `lectures` (1) <---> (M) `study_materials`
- `courses` (1) <---> (M) `batches`
- `batches` (M) <---> (M) `batch_students` (via `enrollments`)
- `batches` (1) <---> (M) `assignments`
- `assignments` (1) <---> (M) `submissions`
- `batches` (1) <---> (M) `quizzes`
- `quizzes` (1) <---> (M) `questions` <---> (M) `quiz_options`
- `quizzes` (1) <---> (M) `quiz_attempts` <---> (M) `quiz_answers`
- `batches` (1) <---> (M) `attendance`
- `students` (1) <---> (M) `lecture_progress`
- `students` (1) <---> (M) `certificates`
- `students` (1) <---> (M) `payments`
- `users` (1) <---> (M) `notifications`
- `announcements` (broadcast / role / batch targeting)
