# LMS Known Issues & Technical Limitations Log

**Document Version:** 1.1  
**Last Updated:** 2026-11-25  

---

## 1. Resolved Issues During Implementation
1. **Pydantic EmailStr Dependency:** Pydantic v2 requires `email-validator` for EmailStr resolution. Resolved by adding `email-validator>=2.1.0` to backend requirements.
2. **SQLAlchemy Join Query in Progress Service:** Resolved relationship join expression to extract enrolled course IDs via mapped batch foreign keys instead of passing in-memory list to `.join()`.
3. **Frontend Login Relative Import:** Corrected relative import path for AuthContext from `src/pages/auth/Login.jsx` to `../../context/AuthContext`.

## 2. Platform & Hosting Operational Notes
1. **MySQL 8.0 Inactivity Timeout:** In cloud deployment (e.g. AWS RDS or PlanetScale), ensure `pool_recycle=3600` is enabled in SQLAlchemy engine to recycle stale idle connections.
2. **Object Storage in Production:** For multi-instance deployment on Render/AWS, configure S3/Cloudflare R2 storage credentials in `.env` to replace local `uploads/` directory persistence.
