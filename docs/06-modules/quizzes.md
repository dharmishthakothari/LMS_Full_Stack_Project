# Quiz & Examination Assessment Engine

## 1. Overview
Automates multiple-choice assessments with timed test-taking, randomized option ordering, answer confidentiality, and instantaneous server-side score calculation.

## 2. Technical Specifications
- **Models**: `Quiz`, `Question`, `QuizOption`, `QuizAttempt`, `QuizAnswer`.
- **Confidentiality Rule**: The API strictly omits `is_correct` flags when delivering questions to student clients. Correctness is evaluated exclusively on the server upon submission.
- **Pass Policy**: Configurable passing percentage (default: 60%).

## 3. Endpoints Implemented
- `GET /api/quizzes`: List quizzes filtered by batch or course.
- `POST /api/quizzes`: Instructor creates timed quiz with passing thresholds.
- `GET /api/quizzes/{id}`: Detailed quiz overview and previous student attempts.
- `POST /api/quizzes/{id}/questions`: Add MCQs with 4 options and mark the correct key.
- `POST /api/quizzes/{id}/start`: Initialize timed attempt and receive question set without answer keys.
- `POST /api/quizzes/attempts/{attempt_id}/submit`: Transmit student answers, execute automated scoring, record score and pass/fail state.
- `GET /api/quizzes/attempts/{attempt_id}/result`: View final score, percentage, and review permitted solutions.

## 4. Frontend Integration
- Views: `QuizList.jsx` and `QuizAttempt.jsx` featuring dynamic timer countdown, option radio selectors, and instant grade summary.
