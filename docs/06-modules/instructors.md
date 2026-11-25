# Instructor Profile Module

## 1. Overview
Manages faculty profiles, educational qualifications, subject specializations, bios, and assigned batches.

## 2. Technical Specifications
- **Models**: `Instructor` table with `1:1` relationship to `User`, `1:N` to `Batch`.
- **Fields**: `employee_code` (unique), `specialization`, `qualification`, `bio`, `years_of_experience`.

## 3. Endpoints Implemented
- `GET /api/instructors`: List all faculty members with active teaching assignments.
- `GET /api/instructors/{id}`: Retrieve detailed instructor curriculum and batch records.
- `PUT /api/instructors/{id}`: Update instructor specialization and bio.
- `GET /api/instructors/me`: Dedicated instructor profile endpoint.
