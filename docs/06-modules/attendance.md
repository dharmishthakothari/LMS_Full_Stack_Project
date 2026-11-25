# Attendance Management Module

## 1. Overview
Manages daily classroom attendance, tracking student participation states (PRESENT, ABSENT, LATE, EXCUSED) with audit trails.

## 2. Technical Specifications
- **Model**: `Attendance` (unique compound index on `batch_id`, `student_id`, `date`).
- **Policy**: Institute requires minimum 75% attendance for graduation and certificate generation.

## 3. Endpoints Implemented
- `GET /api/attendance`: Filter attendance by batch, student, date range.
- `POST /api/attendance/bulk`: Record or update batch roster attendance in a single transaction.
- `GET /api/attendance/summary/{batch_id}`: Aggregate batch attendance statistics.
- `GET /api/attendance/student/{student_id}`: Comprehensive student attendance history and percentage.

## 4. Frontend Integration
- View: `AttendancePage.jsx` supporting date picker, multi-status radio groups, and instant percentage calculation.
