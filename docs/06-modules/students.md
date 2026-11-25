# Student Profile Module

## 1. Overview
Manages student educational records, roll numbers, guardian contact details, enrollment histories, and academic standings.

## 2. Technical Specifications
- **Models**: `Student` table with `1:1` relationship to `User`, `1:N` to `Enrollment`.
- **Fields**: `roll_number` (unique), `guardian_name`, `guardian_phone`, `address`, `date_of_birth`, `education_qualification`.

## 3. Endpoints Implemented
- `GET /api/students`: List and search students across batches (Admin, Instructor).
- `GET /api/students/{id}`: Detailed academic history, enrolled batches, progress metrics.
- `PUT /api/students/{id}`: Update student profile details.
- `GET /api/students/me`: Dedicated profile endpoint for enrolled student self-service.
