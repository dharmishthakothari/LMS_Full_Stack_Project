# Notifications & Announcements Module

## 1. Overview
Facilitates institute-wide bulletins and personalized student/faculty alerts for lecture reschedules, assignment releases, and grades.

## 2. Technical Specifications
- **Models**: `Notification`, `Announcement`.
- **Announcement Scope**: Target audience (`ALL`, `STUDENTS`, `INSTRUCTORS`, `BATCH_SPECIFIC`).
- **Read State**: Notifications track `is_read` boolean per recipient.

## 3. Endpoints Implemented
- `GET /api/notifications`: Retrieve current authenticated user's notifications.
- `PUT /api/notifications/{id}/read`: Mark notification as read.
- `PUT /api/notifications/read-all`: Mark all notifications as read.
- `GET /api/announcements`: Retrieve announcements relevant to the user's role and enrolled batches.
- `POST /api/announcements`: Publish announcement (Admin / Instructor).

## 4. Frontend Integration
- Views: `Header.jsx` quick notification drawer, `NotificationsPage.jsx`, and `AnnouncementsPage.jsx`.
