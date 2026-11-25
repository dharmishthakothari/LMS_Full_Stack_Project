# Lecture & Study Material Module

## 1. Overview
Facilitates live class delivery, recorded video links, downloadable notes, slide decks, and lecture completion tracking.

## 2. Technical Specifications
- **Models**: `Lecture`, `StudyMaterial`, `LectureProgress`.
- **Permissions**: Instructors and Admins manage lectures; Students access authorized batch content and record completion.

## 3. Endpoints Implemented
- `GET /api/batches/{batch_id}/lectures`: List sequential lectures in batch.
- `POST /api/batches/{batch_id}/lectures`: Create lecture with video URL and notes.
- `GET /api/lectures/{id}`: Detailed lecture viewing room with player and resources.
- `PUT /api/lectures/{id}`: Edit lecture details.
- `POST /api/lectures/{id}/materials`: Upload learning resources and supplementary files.
- `POST /api/lectures/{id}/complete`: Student marks lecture as completed.

## 4. Frontend Integration
- View: `LectureRoom.jsx` with embedded video player, resource downloader, and completion toggles.
