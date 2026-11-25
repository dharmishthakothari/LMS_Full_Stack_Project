# LMS REST API Documentation & Endpoint Specification

**Document Version:** 1.1  
**Base URL:** `http://localhost:8000/api`  
**Interactive Docs:** `http://localhost:8000/docs` (Swagger UI) & `/redoc`  
**Authentication Scheme:** HTTP Bearer JWT Header (`Authorization: Bearer <TOKEN>`)  

---

## 1. Authentication (`/api/auth`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `POST` | `/api/auth/login` | Public | Authenticates user credentials, returns JWT access token and user profile |
| `GET` | `/api/auth/me` | Authenticated | Retrieves current user session identity and profile |
| `POST` | `/api/auth/change-password` | Authenticated | Updates account password after validating old password |
| `POST` | `/api/auth/forgot-password` | Public | Dispatches password reset link |
| `POST` | `/api/auth/reset-password` | Public | Consumes reset token and resets password |
| `POST` | `/api/auth/logout` | Authenticated | Terminates user session |

---

## 2. User & Profile Management (`/api/users`, `/api/students`, `/api/instructors`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/users` | Admin | Search, filter, and paginate institute users |
| `POST` | `/api/users` | Admin | Create new user with role assignment and specific profile |
| `GET` | `/api/users/{id}` | Admin | Get detailed user record |
| `PUT` | `/api/users/{id}` | Admin | Update user information or status |
| `DELETE` | `/api/users/{id}` | Admin | Deactivate user account |
| `GET` | `/api/students` | Admin, Instructor | List student profiles and batch affiliations |
| `GET` | `/api/students/{id}` | Admin, Instructor, Self | View student academic record |
| `GET` | `/api/instructors` | Admin, Instructor | List instructors and domain expertise |
| `GET` | `/api/instructors/{id}` | Authenticated | View instructor details and assigned batches |

---

## 3. Curriculum & Batches (`/api/courses`, `/api/modules`, `/api/batches`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/courses` | Authenticated | List all active/published courses |
| `POST` | `/api/courses` | Admin | Create course with tuition fee, code, and duration |
| `GET` | `/api/courses/{id}` | Authenticated | Detailed course syllabus with modules and lectures |
| `PUT` | `/api/courses/{id}` | Admin | Update course metadata |
| `DELETE` | `/api/courses/{id}` | Admin | Delete course or archive if dependencies exist |
| `POST` | `/api/modules` | Admin, Instructor | Add structured module to a course |
| `PUT` | `/api/modules/{id}` | Admin, Instructor | Update module title/sequence |
| `DELETE` | `/api/modules/{id}` | Admin | Remove module |
| `GET` | `/api/batches` | Authenticated | List batches (scoped by role: all for Admin, assigned for Instructor, enrolled for Student) |
| `POST` | `/api/batches` | Admin | Create batch cohort with dates, timings, capacity |
| `GET` | `/api/batches/{id}` | Authenticated | Batch roster and schedule details |
| `PUT` | `/api/batches/{id}` | Admin | Update batch parameters |
| `POST` | `/api/batches/{id}/students` | Admin | Enroll student into batch (checks capacity and duplicates) |
| `DELETE` | `/api/batches/{id}/students/{sid}` | Admin | Drop student from batch |

---

## 4. Lectures & Learning Media (`/api/lectures`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/lectures` | Authenticated | List lectures by module or batch |
| `POST` | `/api/lectures` | Admin, Instructor | Create new lecture |
| `GET` | `/api/lectures/{id}` | Authenticated | Detailed lecture with stream URL, notes, and completion flag |
| `POST` | `/api/lectures/{id}/complete` | Student | Mark lecture completed (records in `lecture_progress`) |
| `POST` | `/api/lectures/{id}/materials` | Admin, Instructor | Upload study materials (PDF/PPT) |

---

## 5. Assignments & Submissions (`/api/assignments`, `/api/submissions`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/assignments` | Authenticated | List assignments for batch/student |
| `POST` | `/api/assignments` | Admin, Instructor | Author assignment with max marks, instructions, due date |
| `GET` | `/api/assignments/{id}` | Authenticated | Detailed assignment with student submission or all submissions |
| `POST` | `/api/submissions` | Student | Multipart submission upload with timestamp |
| `POST` | `/api/submissions/{id}/evaluate` | Admin, Instructor | Input marks obtained and qualitative feedback |

---

## 6. Timed Quizzes & Examination Engine (`/api/quizzes`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/quizzes` | Authenticated | List published assessments and personal attempt history |
| `POST` | `/api/quizzes` | Admin, Instructor | Create MCQ quiz with questions, options, passing criteria |
| `GET` | `/api/quizzes/{id}` | Authenticated | Retrieve quiz. Correct answers hidden from students |
| `POST` | `/api/quizzes/{id}/start` | Student | Initialize attempt and record start timestamp |
| `POST` | `/api/quizzes/submit` | Student | Submit answer sheet; backend calculates score and pass/fail |
| `GET` | `/api/quizzes/attempts/{id}` | Authenticated | View validated attempt scorecard |

---

## 7. Attendance & Academic Progress (`/api/attendance`, `/api/progress`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `POST` | `/api/attendance` | Admin, Instructor | Upsert batch session attendance with audit trail |
| `GET` | `/api/attendance/batch/{id}` | Admin, Instructor | Query session logs for a batch |
| `GET` | `/api/attendance/student/{id}` | Authenticated | Summary percentage and session attendance history |
| `GET` | `/api/progress/me` | Student | Convenience endpoint to retrieve logged-in student's course progress |
| `GET` | `/api/progress/student/{id}` | Authenticated | Calculate weighted dynamic learning progress (Lectures 40%, Assignments 30%, Quizzes 30%) |

---

## 8. Certificates & Public Verification (`/api/certificates`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/certificates` | Authenticated | List issued completion credentials |
| `POST` | `/api/certificates/generate` | Authenticated | Generates certificate PDF if student fulfills all eligibility benchmarks |
| `GET` | `/api/certificates/{id}/download` | Authenticated | Stream / download high-resolution PDF certificate |
| `GET` | `/api/certificates/verify/{vid}` | Public | Cryptographic authenticity verification by unique code |

---

## 9. Payments & PDF Receipts (`/api/payments`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/payments` | Authenticated | Financial ledger entries (scoped by user role) |
| `POST` | `/api/payments` | Admin | Record fee collection, recompute balance, and generate PDF receipt |
| `GET` | `/api/payments/student/{id}/summary` | Authenticated | Aggregate fee summary: total fee, total paid, outstanding balance |
| `GET` | `/api/payments/{id}/receipt` | Authenticated | Download official PDF payment receipt |

---

## 10. Communications & Analytics (`/api/notifications`, `/api/announcements`, `/api/reports`)
| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| `GET` | `/api/notifications` | Authenticated | List in-app alerts |
| `PUT` | `/api/notifications/{id}/read` | Authenticated | Mark individual notification read |
| `PUT` | `/api/notifications/read-all` | Authenticated | Mark all notifications read |
| `GET` | `/api/announcements` | Authenticated | List notices targeted to role or batch |
| `POST` | `/api/announcements` | Admin, Instructor | Publish announcement |
| `GET` | `/api/reports/dashboard` | Authenticated | Role-tailored dynamic KPI metrics and Recharts series (database-derived) |
| `GET` | `/api/reports/export/csv` | Admin, Instructor | Export tabular CSV reports for Students, Payments, Attendance, Courses |
| `GET` | `/api/reports/export/excel` | Admin, Instructor | Export styled Excel (.xlsx) reports |
| `GET` | `/api/reports/export/pdf` | Admin, Instructor | Export landscape PDF summary reports |
| `GET` | `/api/health` | Public | System status and MySQL connectivity health check |
