# Assignment & Submission Module

## 1. Overview
Enables instructors to post homework and capstone projects, and allows students to submit code/documents and receive graded feedback.

## 2. Technical Specifications
- **Models**: `Assignment`, `AssignmentSubmission`, `AssignmentFeedback`.
- **File Constraints**: Max 10MB per file; allowed types `.pdf`, `.zip`, `.py`, `.js`, `.txt`, `.docx`.
- **Scoring**: Max marks defined per assignment; instructors provide marks and qualitative feedback.

## 3. Endpoints Implemented
- `GET /api/assignments`: List assignments filtered by batch.
- `POST /api/assignments`: Instructors create assignment with due dates.
- `GET /api/assignments/{id}`: View assignment guidelines and attached reference files.
- `POST /api/assignments/{id}/submit`: Student uploads file submission.
- `GET /api/assignments/{id}/submissions`: Instructor reviews submitted work.
- `POST /api/submissions/{id}/evaluate`: Grade submission with marks and feedback comments.

## 4. Frontend Integration
- View: `AssignmentList.jsx` featuring tabbed views for pending tasks, submission modal, and evaluation drawer.
