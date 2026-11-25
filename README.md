# Enterprise Learning Management System (LMS)

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.110+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2019%20+%20Vite-61DAFB?style=flat&logo=react)](https://react.dev)
[![MySQL](https://img.shields.io/badge/Database-MySQL%208.0-4479A1?style=flat&logo=mysql)](https://www.mysql.com)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![Pytest](https://img.shields.io/badge/Tests-16%20Passed%20(100%25)-brightgreen?style=flat&logo=pytest)](https://pytest.org)

A centralized, database-driven Learning Management System (LMS) for academic institutions, trainers, and students. Built with **Python FastAPI**, **SQLAlchemy ORM**, **MySQL 8.0**, and **React.js + Tailwind CSS**.

---

## 🚀 Key Features

### 1. Role-Based Access Control (RBAC)
- **Admin Portal:** Institute-wide KPI dashboards, user account lifecycle (Admin, Instructor, Student), course curriculum structuring, batch scheduling with capacity constraints, fee installment ledgers, announcements, and CSV report exports.
- **Instructor Portal:** Scoped strictly to assigned batches and courses. Lecture and learning material publishing, assignment authoring and grading, timed MCQ quiz creation, and daily batch attendance logging.
- **Student Portal:** Access restricted to personal enrolled courses. Video classroom with notes downloads, lecture completion progress tracking, assignment submission, timed quiz examination interface, fee history, and verified completion certificate downloads.

### 2. High-Integrity Assessment & Examination Engine
- **Timed MCQ Quizzes:** Server-enforced timers, answer secrecy (correct answers never exposed to client prior to submission), and server-side score calculation.
- **Coursework Submissions:** File deliverables with deadline enforcement, versioning, and instructor qualitative critique.

### 3. Dynamic Academic Progress Tracking
$$\text{Progress} = (0.40 \times \text{Lectures}) + (0.30 \times \text{Assignments}) + (0.30 \times \text{Quizzes})$$
- Automatically evaluates certificate eligibility upon reaching **≥ 80% course progress**, **≥ 75% attendance**, and **zero fee balance**.

### 4. Automated PDF Generation & Verification
- **Payment Receipts:** Official PDF tuition fee receipts with transaction references.
- **Course Certificates:** High-resolution completion credentials with unique verification IDs verifiable at `/verify-certificate`.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite, Tailwind CSS, Lucide Icons, Recharts, React Router DOM, Axios |
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy 2.0 ORM, Pydantic v2, PyMySQL, Alembic |
| **Database** | MySQL 8.0 (UTF8mb4 character set, InnoDB, Foreign Keys) |
| **Authentication** | JSON Web Tokens (JWT), Bcrypt password hashing |
| **PDF Generation** | ReportLab PDF engine |
| **Automated Testing**| Pytest, FastAPI TestClient, Starlette HTTPX |

---

## 🔑 Demonstration Accounts

The database comes pre-seeded with synthetic demonstration accounts:

| Role | Email | Password | Scope |
|---|---|---|---|
| **Admin** | `admin@lms.com` | `Admin@123` | Institute-wide Superuser |
| **Instructor** | `dr.patel@lms.com` | `Instructor@123` | Full Stack Web Track Faculty |
| **Instructor** | `er.verma@lms.com` | `Instructor@123` | Cloud & DevOps Faculty |
| **Instructor** | `prof.sharma@lms.com` | `Instructor@123` | Data Science Faculty |
| **Student** | `student1@lms.com` | `Student@123` | Enrolled Learner (Cert Eligible) |
| **Student** | `student2@lms.com` ... `student10@lms.com` | `Student@123` | Enrolled Learners |

*Tip: The login page provides quick one-click buttons to sign in as Admin, Instructor, or Student instantly.*

---

## 💻 Installation & Quickstart

### 1. Prerequisites
- **Python 3.11+**
- **Node.js v18+** & npm
- **MySQL 8.0** running locally on port `3306`

### 2. Backend Setup
```powershell
# Navigate to backend
cd backend

# Create virtual environment and activate
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and seed synthetic records
python init_db.py
python seed_data.py

# Start FastAPI REST API Server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Server: `http://localhost:8000`
- Interactive Swagger API Documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. Frontend Setup
```powershell
# In a separate terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start Vite Development Server
npm run dev
```
- Frontend Web Portal: `http://localhost:5173`

---

## 🧪 Automated Testing

Execute the automated Pytest test suite:
```powershell
cd backend
.\venv\Scripts\pytest.exe -v
```
**Test Results:** 16 tests executed, **16 passed (100% success rate)** covering authentication, authorization (RBAC), database constraints, assessment scoring, and public verification.

---

## 📁 Repository Structure
```
LMS_Application_With_Vibe/
├── backend/
│   ├── app/
│   │   ├── models/              # 24 SQLAlchemy entities
│   │   ├── routers/             # 51 REST API routes
│   │   ├── schemas/             # Pydantic validation models
│   │   ├── services/            # PDF generation & progress engine
│   │   ├── dependencies/        # JWT & RBAC dependencies
│   │   └── main.py              # App entry point
│   ├── migrations/              # Alembic migration revisions
│   ├── tests/                   # Pytest automated test suites
│   ├── init_db.py               # Database initialization
│   ├── seed_data.py             # Synthetic demonstration records
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI widgets (DataTable, StatCard, Modal)
│   │   ├── context/             # AuthContext session management
│   │   ├── layouts/             # DashboardLayout with role navigation
│   │   ├── pages/               # 42 functional screen views
│   │   └── App.jsx              # Role-guarded routing
│   └── package.json
└── docs/                        # Complete 22-document system specifications
    ├── 01-requirements/         # SRS notes & use cases
    ├── 02-design/               # Data dictionary & database design
    ├── 03-business-rules/       # Academic & financial policies
    ├── 04-architecture/         # Architecture & security specifications
    ├── 05-api/                  # Endpoint catalog & Postman collection
    ├── 08-testing/              # Test plan, report & known issues
    ├── 09-deployment/           # Deployment, env guide & backup procedures
    ├── 10-user-manual/          # Admin, Instructor, Student guides
    └── 11-reports/              # Progress log, changelog, viva prep & final report
```

---

## 📜 License
Educational & Institute Use Only • Developed according to LMS SRS Version 1.1 Specifications.
