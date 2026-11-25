# Course & Curriculum Module

## 1. Overview
Enables course catalog management, syllabus structuring through modules, duration, and fee configurations.

## 2. Technical Specifications
- **Models**: `Course`, `CourseModule`.
- **Relationships**: A Course has many `CourseModule`s and `Batch`es.
- **Rules**: Courses cannot be deleted if active batches or enrolled students exist.

## 3. Endpoints Implemented
- `GET /api/courses`: List public and institute courses with search and filters.
- `POST /api/courses`: Admin creation of new courses.
- `GET /api/courses/{id}`: Detailed course view including syllabus tree and module breakdown.
- `PUT /api/courses/{id}`: Update course metadata, fees, and objectives.
- `DELETE /api/courses/{id}`: Soft delete or decommission course.
- `GET /api/courses/{id}/modules`: Retrieve all syllabus modules for a course.
- `POST /api/courses/{id}/modules`: Add curriculum module to course.

## 4. Frontend Integration
- Views: `CourseList.jsx`, `CourseDetail.jsx`.
