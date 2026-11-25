# LMS Test Execution Report

**Document Version:** 1.1  
**Executed By:** Antigravity Autonomous QA Harness  
**Date of Execution:** 2026-11-25  
**Execution Status:** PASSED (16 of 16 tests passing, 100% success rate)  

---

## 1. Summary of Execution
| Category | Tests Executed | Passed | Failed | Status |
|---|---|---|---|---|
| Authentication & Sessions | 5 | 5 | 0 | PASSED |
| Role-Based Authorization (RBAC) | 4 | 4 | 0 | PASSED |
| Courses & Batch Constraints | 3 | 3 | 0 | PASSED |
| Assignments, Quizzes & Verification | 4 | 4 | 0 | PASSED |
| **Total** | **16** | **16** | **0** | **100% PASSED** |

---

## 2. Detailed Test Results Log
| Test Case ID | Test Identifier | Module | Description | Expected Status | Actual Status | Result |
|---|---|---|---|---|---|---|
| TC-AUTH-01 | `test_valid_admin_login` | Auth | Login with valid admin credentials returns signed JWT | 200 OK | 200 OK | PASS |
| TC-AUTH-02 | `test_invalid_password` | Auth | Incorrect password fails with 401 | 401 Unauthorized | 401 Unauthorized | PASS |
| TC-AUTH-03 | `test_nonexistent_user` | Auth | Ghost email fails with 401 | 401 Unauthorized | 401 Unauthorized | PASS |
| TC-AUTH-04 | `test_get_current_user_profile` | Auth | Authenticated token resolves current user | 200 OK | 200 OK | PASS |
| TC-AUTH-05 | `test_health_check` | Health | Health endpoint confirms MySQL connectivity | 200 OK | 200 OK | PASS |
| TC-RBAC-01 | `test_student_forbidden_from_users_list` | RBAC | Student querying `/api/users` is blocked | 403 Forbidden | 403 Forbidden | PASS |
| TC-RBAC-02 | `test_instructor_forbidden_from_creating_user` | RBAC | Faculty creating user is blocked | 403 Forbidden | 403 Forbidden | PASS |
| TC-RBAC-03 | `test_student_forbidden_from_recording_payments` | RBAC | Student posting to `/api/payments` is blocked | 403 Forbidden | 403 Forbidden | PASS |
| TC-RBAC-04 | `test_admin_allowed_to_view_all_users` | RBAC | Admin querying `/api/users` succeeds | 200 OK | 200 OK | PASS |
| TC-CRS-01 | `test_list_courses` | Courses | Student retrieves published courses | 200 OK | 200 OK | PASS |
| TC-CRS-02 | `test_create_course_admin` | Courses | Admin creates new curriculum record | 200 OK | 200 OK | PASS |
| TC-BAT-01 | `test_batch_date_validation` | Batches | Batch with end_date < start_date rejected | 400 Bad Request | 400 Bad Request | PASS |
| TC-ASM-01 | `test_assignment_evaluation_marks_validation` | Assignments | Evaluation marks exceeding max_marks rejected | 400 Bad Request | 400 Bad Request | PASS |
| TC-QZ-01 | `test_student_quiz_answers_secrecy` | Quizzes | Student fetching quiz options does NOT receive `is_correct` | 200 OK | 200 OK | PASS |
| TC-PRG-01 | `test_attendance_and_progress` | Progress | Student progress is dynamically calculated | 200 OK | 200 OK | PASS |
| TC-CRT-01 | `test_public_certificate_verification` | Certificates | Public verification confirms authentic certificate | 200 OK | 200 OK | PASS |
