# Learning Management System (LMS) - Final Project Report

**Document Version:** 1.1  
**Project:** Role-Based Full Stack Learning Management System  
**Submission Date:** 2026-11-25  

---

## 1. Executive Summary
The Learning Management System (LMS) is a production-ready, database-driven web application architected to centralize academic operations, course curriculum delivery, faculty management, student tracking, attendance auditing, digital credential issuance, and fee tracking for an enterprise training institute.

The system strictly implements the requirements outlined in the **LMS Full Stack Project Assignment & SRS Version 1.1**.

## 2. Key Highlights & Achievements
- **Strict Role-Based Access Control (RBAC):** Backend-enforced authorization across Admin, Instructor, and Student roles with JWT token authentication and Bcrypt hashing.
- **Relational Persistence in MySQL 8.0:** 24 relational tables connected via SQLAlchemy 2.0 ORM with primary keys, foreign keys, unique composite constraints, and Alembic database versioning.
- **Academic Assessment Engine:**
  - Assignments with deadline validation, versioned submissions, marks validation, and qualitative feedback.
  - Timed MCQ Quizzes with anti-tamper answer secrecy (correct answers never sent to frontend), live countdown timer, and server-side scoring.
- **Dynamic Academic Progress Formula:** Real-time calculation based on 40% lecture completion, 30% assignment evaluation, and 30% quiz results.
- **Automated PDF Generation:** ReportLab generator for high-resolution Completion Certificates and official Payment Receipts.
- **Interactive UI/UX:** Responsive SaaS interface built with React 19, Tailwind CSS, Lucide Icons, and Recharts analytics visualizations.
- **100% Automated Test Pass Rate:** 16 automated Pytest integration and security tests verified.
