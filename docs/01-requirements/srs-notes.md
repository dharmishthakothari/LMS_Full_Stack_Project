# Learning Management System (LMS) - SRS Notes & Requirement Analysis

**Document Version:** 1.1  
**Author:** Software Architecture Team  
**Last Updated:** 2026-11-25  
**Project Status:** Active Development  

---

## 1. System Vision & Objective
The Learning Management System (LMS) is a centralized, role-based, database-driven web application designed for a premier training institute. The system orchestrates academic administration, curriculum delivery, assessment management, student tracking, attendance audits, digital certificate issuance, fee tracking, and institutional analytics.

## 2. Core Stakeholders & Role Analysis
1. **Admin (Super Administrator / Academic Director)**
   - Institute-wide operational visibility and governance.
   - User account lifecycle management (Students, Instructors, Staff).
   - Curriculum administration (Courses, Modules, Syllabi).
   - Batch scheduling, instructor assignment, student enrollment.
   - Financial ledger management (Course fees, installment tracking, manual receipt generation).
   - Institutional announcements and system-wide analytical reports.
   
2. **Instructor (Faculty / Trainer)**
   - Scoped strictly to assigned courses and batches.
   - Structured lecture creation and multimedia learning material publishing.
   - Assignment authoring, deadline enforcement, evaluation, grading, and qualitative feedback.
   - Quiz creation (MCQs), scheduling, passing criteria, and attempt audits.
   - Daily attendance logging with immutable audit records.
   - Batch progress tracking and academic reporting.

3. **Student (Learner)**
   - Scoped strictly to personal account and enrolled courses/batches.
   - Structured curriculum access (Lectures, Notes, PPTs, Reference videos).
   - Mark lectures completed with automatic progress bar updates.
   - Assignment submission with versioning and feedback review.
   - Interactive timed MCQ examination attempts with instant server-calculated score and answer reviews.
   - Personal attendance percentage and calendar tracking.
   - Financial ledger review and PDF receipt downloads.
   - Verified PDF Certificate downloads upon reaching course completion thresholds.

---

## 3. Scope Boundaries

### 3.1 In-Scope Deliverables
- Multi-role JWT authentication with Argon2/Bcrypt password hashing.
- Role-Based Access Control (RBAC) enforced strictly at the database/API layer.
- Course, Module, and Batch hierarchical scheduling.
- Student enrollment with capacity validation and duplicate prevention.
- Lecture and multimedia study material repository with secure file streaming.
- Assignment lifecycle (Creation -> Submission -> Review -> Grade & Feedback).
- Robust MCQ Quiz Engine with backend timestamp verification, timers, and server-side scoring.
- Batch Attendance system with attendance percentage calculation and audit history.
- Dynamic student progress calculation based on real academic actions.
- Automated PDF Certificate generation with unique verification hashes and public verification endpoint.
- Course fee management with installment support, balance calculation, and PDF receipts.
- Real-time in-app notifications and targeted role/batch announcements.
- Institutional analytics dashboards with Recharts visualizations and CSV/Excel exports.

### 3.2 Out-of-Scope (Version 1.1)
- Automated third-party payment gateway settlement (Razorpay/Stripe automated callbacks reserved for future phase; manual administrative entries and receipts implemented).
- In-house WebRTC live streaming (supported via external video URL embedding and uploaded video streaming).
- Native iOS/Android apps (responsive web design supports all modern mobile browsers).
- AI automatic grading or biometric face detection.

---

## 4. Key Architectural Assumptions
1. **Database:** MySQL 8.0+ running with InnoDB, UTF8mb4 character set, and foreign key enforcement.
2. **Persistence Guarantee:** No mock data or in-memory arrays; all data flows from MySQL via SQLAlchemy ORM.
3. **Session Management:** Stateless JWT with configurable expiration and secure HTTP headers.
4. **Timezone Uniformity:** All database timestamps stored in UTC and rendered in local client time.
