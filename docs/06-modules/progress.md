# Student Progress Calculation Engine

## 1. Overview
Computes holistic student academic progression through weighted completion metrics across three core pillars: Lectures, Assignments, and Quizzes.

## 2. Formula & Weightage
$$\text{Progress} = (0.40 \times \text{Lecture \%}) + (0.30 \times \text{Assignment \%}) + (0.30 \times \text{Quiz \%})$$

- **Lecture Completion**: Percentage of batch lectures marked as completed by student.
- **Assignment Completion**: Percentage of required assignments submitted and accepted.
- **Quiz Performance**: Average score percentage across all batch quizzes.

## 3. Endpoints Implemented
- `GET /api/progress/student/{student_id}`: Comprehensive breakdown of student progress across all enrolled batches.
- `GET /api/progress/batch/{batch_id}`: Batch-wide progress ledger comparing all enrolled students.
- `GET /api/progress/me`: Student self-service progress inquiry.

## 4. Frontend Integration
- View: `ProgressPage.jsx` with visual progress bars, completion gauges, and breakdown cards.
