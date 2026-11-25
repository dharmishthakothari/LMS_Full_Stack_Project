# Environment Variables & Configuration Guide

This guide details all environment variables required to run, test, and deploy both the Backend (FastAPI) and Frontend (React/Vite) applications.

---

## 1. Backend Environment Variables (`backend/.env`)

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | String | `LMS Platform` | Application title reported in Swagger UI and OpenAPI specifications. |
| `VERSION` | String | `1.0.0` | Semantic version string. |
| `DEBUG` | Boolean | `False` | Enables debug logging and automatic reload when true. |
| `DATABASE_URL` | String | `mysql+pymysql://root:root@localhost:3306/lms_db` | MySQL connection string. If unreachable, system falls back to `sqlite:///./lms.sqlite3`. |
| `TEST_DATABASE_URL` | String | `mysql+pymysql://root:root@localhost:3306/lms_test_db` | Dedicated clean database for Pytest test runs. |
| `SECRET_KEY` | String | *(Random 32-char hex)* | Cryptographic key used to sign and verify JWT tokens. |
| `ALGORITHM` | String | `HS256` | JWT signing algorithm. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Integer | `480` | JWT validity duration (8 hours). |
| `UPLOAD_DIR` | String | `uploads` | Local or mounted filesystem path where submitted files and PDFs are saved. |
| `MAX_UPLOAD_SIZE_MB` | Integer | `10` | Maximum file upload size limit in megabytes. |
| `ALLOWED_EXTENSIONS` | List[String] | `pdf,zip,png,jpg,docx,txt,py` | Whitelist of permitted file extensions for submissions and materials. |
| `CORS_ORIGINS` | List[String] | `http://localhost:5173,http://localhost:3000` | Allowed origins for Cross-Origin Resource Sharing. |
| `RATE_LIMIT_PER_MINUTE` | Integer | `120` | Max requests per minute per IP address before rate limiting activates. |

---

## 2. Frontend Environment Variables (`frontend/.env`)

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `VITE_API_BASE_URL` | String | `http://localhost:8000/api` | Absolute URL to the FastAPI backend API prefix. |
| `VITE_APP_TITLE` | String | `LMS - Learning Management System` | Browser tab title and application brand name. |

---

## 3. Quick Start Setup

### Backend
```bash
cd backend
cp .env.example .env
# Adjust DATABASE_URL with your local MySQL credentials
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python seed_data.py
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```
