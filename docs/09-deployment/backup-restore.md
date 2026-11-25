# LMS Database Backup & Disaster Recovery Procedure

**Document Version:** 1.1  
**Last Updated:** 2026-11-25  

---

## 1. Automated Backup Policy
- **Frequency:** Daily automated snapshots at 02:00 UTC.
- **Retention Period:** 30 days rolling retention.
- **Storage:** Encrypted multi-region object storage.

## 2. Manual Backup Command (mysqldump)
To perform an immediate hot backup of the production LMS database:
```powershell
# Export complete schema and data with transactions enabled
mysqldump -u root -p --single-transaction --routines --triggers --databases lms_db > lms_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql
```

## 3. Restoration Procedure
To restore from an SQL dump in event of disaster recovery:
```powershell
# 1. Create fresh database container
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS lms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. Restore tables and records
mysql -u root -p lms_db < lms_backup_20261125.sql

# 3. Verify Alembic migration head status
cd backend
venv\Scripts\alembic.exe current
```
