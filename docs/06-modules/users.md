# User Management Module

## 1. Overview
Empowers the Administrator to oversee institute staff and student identities, enforce account lifecycles, and handle role assignments.

## 2. Technical Specifications
- **RBAC Rule**: Admin-only access.
- **Persistence Model**: `User` table joined with `Role`.
- **Integrity**: Soft-deletion and account status toggling via `is_active` flag.

## 3. Endpoints Implemented
- `GET /api/users`: Search, filter by role/status, and paginate institute users.
- `POST /api/users`: Admin creation of new users with auto-generated temporary credentials.
- `GET /api/users/{id}`: Detailed user record inspection.
- `PUT /api/users/{id}`: Edit demographic info, role assignment, and phone number.
- `PATCH /api/users/{id}/status`: Toggle user activation status (Active / Inactive).
- `DELETE /api/users/{id}`: Remove or deactivate user account with cascade handling.

## 4. Frontend Integration
- **View**: `UserManagement.jsx` featuring dynamic data table, role badges, status switches, and new user creation modal.
