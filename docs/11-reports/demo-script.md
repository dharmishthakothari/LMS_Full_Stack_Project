# Demo Script & Screenshots Guide

**Document Version:** 1.1  
**Last Updated:** 2026-11-25  

---

## 1. Synthetic Demo Accounts

| Role | Email | Password | Primary Purpose |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@lms.com` | `Admin@123` | Institute KPIs, user/course/batch management, fees, reports |
| **Instructor** | `dr.patel@lms.com` | `Instructor@123` | Assigned batches, lectures, grading, quizzes, attendance |
| **Student** | `student1@lms.com` | `Student@123` | Enrolled courses, lecture completion, submissions, quiz attempt, certificates |

---

## 2. Step-by-Step Live Demonstration Order

1. **Public Entry & Authentication**
   - Open `/login`. Demonstrate 1-click demo selector, validation, and `/forgot-password` flow.
   - Open `/verify-certificate` and verify `CERT-PY-2026-001`.
2. **Admin Walkthrough**
   - Sign in as `admin@lms.com`. Show dynamic KPI cards and Recharts charts on `/admin/dashboard`.
   - Open `/users` to search/filter users and toggle status.
   - Open `/courses` and `/batches` to show course modules, instructor assignment, and batch roster capacity.
   - Open `/payments` and download a ReportLab PDF fee receipt.
   - Open `/reports` and export a dataset in CSV, Excel, or PDF.
3. **Instructor Walkthrough**
   - Sign in as `dr.patel@lms.com`. Show `/instructor/dashboard` (assigned batches, pending evaluations).
   - Open `/assignments` to review a student submission and assign marks/feedback.
   - Open `/attendance` to mark daily batch attendance.
4. **Student Walkthrough**
   - Sign in as `student1@lms.com`. Show `/student/dashboard` (progress, attendance %, upcoming quizzes).
   - Open `/lectures/1` to view study materials and mark a lecture complete.
   - Open `/quizzes` and complete a timed MCQ quiz attempt.
   - Open `/progress` and `/certificates` to verify eligibility and download the PDF certificate.

---

## 3. Recommended Screenshots Checklist (`docs/screenshots/`)
Capture the following screenshots from the live application and save them in `docs/screenshots/`:
- `01-login-page.png`
- `02-admin-dashboard.png`
- `03-instructor-dashboard.png`
- `04-student-dashboard.png`
- `05-courses-and-modules.png`
- `06-batch-roster.png`
- `07-lecture-room.png`
- `08-assignments-evaluation.png`
- `09-quiz-attempt.png`
- `10-attendance-grid.png`
- `11-payments-receipt.png`
- `12-certificate-verify.png`
- `13-reports-export.png`
