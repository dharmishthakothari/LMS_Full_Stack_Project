# Batch & Enrollment Module

## 1. Overview
Manages academic cohorts, scheduling, instructor assignments, student enrollments, and batch capacity controls.

## 2. Technical Specifications
- **Models**: `Batch`, `Enrollment`.
- **Enrollment States**: `ENROLLED`, `COMPLETED`, `DROPPED`.
- **Capacity Enforcement**: Prevents batch enrollment when active enrollments exceed `max_students`.

## 3. Endpoints Implemented
- `GET /api/batches`: List batches filtered by course, instructor, or active state.
- `POST /api/batches`: Create new batch with schedule and instructor assignment.
- `GET /api/batches/{id}`: Batch detail with enrolled student roster and upcoming lectures.
- `PUT /api/batches/{id}`: Update batch schedule, classroom link, or instructor.
- `POST /api/batches/{id}/enroll`: Enroll student into batch.
- `DELETE /api/batches/{id}/enroll/{student_id}`: Remove student from batch.

## 4. Frontend Integration
- Views: `BatchList.jsx`, `BatchDetail.jsx`.
