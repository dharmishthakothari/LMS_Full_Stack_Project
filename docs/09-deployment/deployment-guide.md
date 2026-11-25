# LMS Production Deployment & Infrastructure Guide

**Document Version:** 1.1  
**Last Updated:** 2026-11-25  

---

## 1. Cloud Architecture Overview
- **Frontend SPA:** Live on Netlify: **https://lms-fullstack-platform.netlify.app** with CDN edge distribution and automatic SPA redirect handling via `netlify.toml`.
- **Backend API:** Configured for Render via `render.yaml` and `backend/Procfile` running Python 3.11 with Uvicorn workers.
- **Managed Database:** Persistent MySQL 8.0 instance (AWS RDS, Aiven MySQL, or Clever Cloud MySQL).
- **Persistent Storage:** S3-compatible bucket (or Render persistent disk) for PDF certificates, payment receipts, and uploaded study materials.

---

## 2. Step-by-Step Deployment Procedure

### 2.1 Backend Deployment on Render (1-Click Blueprint)

1. **Connect GitHub to Render:**
   - Go to [https://dashboard.render.com/blueprints/new](https://dashboard.render.com/blueprints/new).
   - Connect your GitHub repository: `https://github.com/dharmishthakothari/LMS_Full_Stack_Project.git`.
   - Render will automatically read the root [`render.yaml`](file:///d:/TOPS%20Technologies/LMS_Application_With_Vibe/render.yaml) file.

2. **Database Provisioning (Hosted MySQL 8.0):**
   - In Render or via a free cloud MySQL provider (e.g. [Aiven.io](https://aiven.io) or [Clever Cloud](https://www.clever-cloud.com)):
     - Create a MySQL 8.0 service.
     - Copy the external connection URI:
       `mysql+pymysql://<user>:<password>@<host>:<port>/<dbname>?charset=utf8mb4`
   - In Render, paste this URI as the value for the `DATABASE_URL` environment variable.

3. **Automatic Environment Variables Managed by `render.yaml`:**
   - `JWT_SECRET`: Generated automatically (cryptographically secure 256-bit).
   - `JWT_ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `1440` (24 Hours)
   - `STORAGE_BACKEND`: `s3` (recommended for persistent production storage; `local` for local dev only)
   - `CORS_ORIGINS`: `https://lms-fullstack-platform.netlify.app,http://localhost:5173`
   - `FRONTEND_URL`: `https://lms-fullstack-platform.netlify.app`

4. **Database Initialization & Seeding on First Launch:**
   - In the Render Web Service Shell / SSH:
     ```bash
     cd backend
     python -m alembic upgrade head
     python seed_data.py
     ```
   - Health check will report healthy at `/api/health`.

### 2.2 Live Frontend Deployment on Netlify

The frontend is live and deployed:
- **Production URL:** `https://lms-fullstack-platform.netlify.app`
- **Build Command:** `npm run build`
- **Publish Directory:** `dist`
- **Environment Variable:** `VITE_API_BASE_URL` points to the live backend API route.
- All downloads use authenticated Axios blob streaming with Bearer token injection.
