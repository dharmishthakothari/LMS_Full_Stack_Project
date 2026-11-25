# LMS Production Deployment & Infrastructure Guide

**Document Version:** 1.1  
**Last Updated:** 2026-11-25  

---

## 1. Cloud Architecture Overview
- **Frontend SPA:** Hosted on Vercel or Netlify with automatic CDN edge caching and client-side URL rewriting (`/* -> /index.html`).
- **Backend API:** Hosted on Render, Railway, or AWS Elastic Beanstalk running Gunicorn/Uvicorn workers.
- **Managed Database:** Persistent MySQL 8.0 instance (AWS RDS, PlanetScale, or Aiven MySQL).
- **Persistent Storage:** Persistent volume or S3-compatible bucket for PDF certificates and receipts.

---

## 2. Step-by-Step Deployment Procedure

### 2.1 Backend Deployment (e.g. Render / AWS)
1. Set Environment Variables in host dashboard:
   - `DATABASE_URL`: `mysql+pymysql://<user>:<password>@<host>:3306/<dbname>?charset=utf8mb4`
   - `JWT_SECRET`: Generate a 64-character random cryptographic secret
   - `CORS_ORIGINS`: `["https://your-frontend.vercel.app"]`
2. Build Command: `pip install -r backend/requirements.txt`
3. Pre-Deploy Migration Command: `cd backend && alembic upgrade head && python seed_data.py`
4. Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Health Check Endpoint: `/api/health`

### 2.2 Frontend Deployment (e.g. Vercel)
1. Root Directory: `frontend`
2. Build Command: `npm run build`
3. Output Directory: `dist`
4. Environment Variables:
   - `VITE_API_BASE_URL`: `https://your-backend.onrender.com/api`
5. SPA Routing: Configure `vercel.json` rewrites:
   ```json
   {
     "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
   }
   ```
