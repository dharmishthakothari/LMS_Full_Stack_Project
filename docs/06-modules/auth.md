# Authentication & Session Module

## 1. Overview
The Authentication module handles identity verification, credential security, role assignment, token issuance, and password recovery across the LMS application.

## 2. Technical Specifications
- **Algorithms**: Bcrypt password hashing (`passlib[bcrypt]`), JWT (`HS256`).
- **Token Lifespan**: Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 480 minutes / 8 hours).
- **Authentication Header**: `Authorization: Bearer <JWT_ACCESS_TOKEN>`.
- **Payload Claims**:
  - `sub`: User email address
  - `id`: Integer primary key ID of user
  - `role`: Role slug (`admin`, `instructor`, `student`)
  - `exp`: Epoch expiration timestamp

## 3. Endpoints Implemented
- `POST /api/auth/login`: Authenticates email and password, verifies account status (`is_active == True`), issues JWT token.
- `POST /api/auth/logout`: Client-side token invalidation and session clearance.
- `GET /api/auth/me`: Decodes bearer token and returns current authenticated user profile and permissions.
- `POST /api/auth/forgot-password`: Generates secure password reset token and dispatches reset instructions.
- `POST /api/auth/reset-password`: Validates token and resets account password with bcrypt hashing.
- `POST /api/auth/change-password`: Authenticated endpoint requiring current password validation before updating to new password.

## 4. Frontend Integration
- **Context**: `AuthContext.jsx` manages token in `localStorage`, decodes role, and attaches Axios authorization interceptors.
- **Components**: `Login.jsx` (includes one-click demo credentials for Admin, Instructor, and Student), `ForgotPassword.jsx`, `ResetPassword.jsx`.
- **Guards**: `Guards.jsx` implements `ProtectedRoute` and `RoleGuard`.
