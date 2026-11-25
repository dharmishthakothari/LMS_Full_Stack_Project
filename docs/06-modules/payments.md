# Fee Payment & Receipt Module

## 1. Overview
Tracks student course tuition fees, installment receipts, transaction logs, payment statuses, and issues digitally signed PDF invoices/receipts.

## 2. Technical Specifications
- **Model**: `Payment`.
- **Statuses**: `PENDING`, `PARTIAL`, `PAID`, `FAILED`, `REFUNDED`.
- **Payment Modes**: `CASH`, `CARD`, `UPI`, `NET_BANKING`, `BANK_TRANSFER`.
- **PDF Generation**: ReportLab engine formats institute receipts with invoice numbers, line items, and institution seals.

## 3. Endpoints Implemented
- `GET /api/payments`: List transactions filtered by student, status, date range.
- `POST /api/payments`: Record payment entry with transaction reference ID.
- `GET /api/payments/{id}`: Detailed receipt view.
- `GET /api/payments/{id}/receipt`: Download official PDF payment receipt.
- `GET /api/payments/student/{student_id}/summary`: Total fees assessed, amount paid, and outstanding balance.

## 4. Frontend Integration
- View: `PaymentPage.jsx` featuring dynamic receipt generator, filterable ledger, and invoice download action.
