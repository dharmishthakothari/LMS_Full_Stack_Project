# Certificate Generation & Verification Module

## 1. Overview
Manages course completion certificates, cryptographic verification codes, automated eligibility auditing, and dynamic high-resolution PDF generation using ReportLab.

## 2. Eligibility Requirements
To generate or claim a certificate:
1. Overall Course Progress $\ge 80\%$
2. Overall Attendance Percentage $\ge 75\%$
3. Fee Payment Status = `PAID` (Zero outstanding balance)

## 3. Endpoints Implemented
- `GET /api/certificates`: List issued certificates (Admin/Instructor: institute-wide, Student: personal).
- `POST /api/certificates/generate`: Validates eligibility criteria and triggers ReportLab PDF rendering with QR code and verification code.
- `GET /api/certificates/{id}/download`: Streams binary PDF document to client.
- `GET /api/certificates/verify/{certificate_code}`: Public endpoint allowing employers and third parties to authenticate certificate validity without login.

## 4. Frontend Integration
- Views: `CertificatePage.jsx` and public `VerifyCertificate.jsx`.
