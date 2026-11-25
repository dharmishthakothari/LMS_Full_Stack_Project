import os
from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.models import Payment, Student, Course, User
from app.schemas.shared import PaymentCreate, PaymentResponse
from app.dependencies.auth import get_current_user, require_role
from app.services.pdf_service import generate_payment_receipt_pdf

router = APIRouter(prefix="/api/payments", tags=["Payments"])

@router.get("")
def list_payments(
    student_id: Optional[int] = None,
    course_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Payment)

    if current_user.role.name == "student":
        if not current_user.student_profile:
            return []
        query = query.filter(Payment.student_id == current_user.student_profile.id)
    elif student_id:
        query = query.filter(Payment.student_id == student_id)

    if course_id:
        query = query.filter(Payment.course_id == course_id)

    payments = query.order_by(Payment.payment_date.desc()).all()
    results = []
    for p in payments:
        results.append({
            "id": p.id,
            "student_id": p.student_id,
            "student_name": f"{p.student.user.first_name} {p.student.user.last_name}",
            "course_id": p.course_id,
            "course_title": p.course.title,
            "total_fee": float(p.total_fee),
            "paid_amount": float(p.paid_amount),
            "pending_amount": float(p.pending_amount),
            "payment_date": p.payment_date.isoformat(),
            "payment_method": p.payment_method,
            "transaction_reference": p.transaction_reference,
            "status": p.status,
            "receipt_path": p.receipt_path,
            "remarks": p.remarks
        })
    return results

@router.post("")
def record_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    course = db.query(Course).filter(Course.id == data.course_id).first()
    student = db.query(Student).filter(Student.id == data.student_id).first()
    if not course or not student:
        raise HTTPException(status_code=404, detail="Student or Course not found.")

    if data.paid_amount <= Decimal("0"):
        raise HTTPException(status_code=400, detail="Payment amount must be greater than zero.")

    # Calculate previously paid amount
    past_payments = db.query(Payment).filter(
        Payment.student_id == data.student_id,
        Payment.course_id == data.course_id,
        Payment.status.in_(["paid", "partially_paid"])
    ).all()
    previously_paid = sum(p.paid_amount for p in past_payments)
    
    total_fee = course.fee
    new_total_paid = previously_paid + data.paid_amount
    pending = max(Decimal("0.00"), total_fee - new_total_paid)
    
    status_str = "paid" if pending == Decimal("0.00") else "partially_paid"

    # Generate PDF receipt
    receipt_meta = {
        "transaction_reference": data.transaction_reference,
        "student_id": student.id,
        "student_name": f"{student.user.first_name} {student.user.last_name}",
        "course_title": course.title,
        "total_fee": total_fee,
        "paid_amount": data.paid_amount,
        "pending_amount": pending,
        "payment_method": data.payment_method
    }
    receipt_url = generate_payment_receipt_pdf(receipt_meta)

    payment = Payment(
        student_id=data.student_id,
        course_id=data.course_id,
        total_fee=total_fee,
        paid_amount=data.paid_amount,
        pending_amount=pending,
        payment_method=data.payment_method,
        transaction_reference=data.transaction_reference,
        status=status_str,
        receipt_path=receipt_url,
        remarks=data.remarks,
        recorded_by_id=current_user.id
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "message": "Payment recorded successfully.",
        "payment_id": payment.id,
        "pending_amount": float(pending),
        "status": status_str,
        "receipt_path": receipt_url
    }

@router.get("/{payment_id}/receipt")
def download_receipt(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found.")

    if current_user.role.name == "student":
        if payment.student_id != current_user.student_profile.id:
            raise HTTPException(status_code=403, detail="Access denied.")

    if not payment.receipt_path:
        # Re-generate on demand
        receipt_meta = {
            "transaction_reference": payment.transaction_reference,
            "student_id": payment.student_id,
            "student_name": f"{payment.student.user.first_name} {payment.student.user.last_name}",
            "course_title": payment.course.title,
            "total_fee": payment.total_fee,
            "paid_amount": payment.paid_amount,
            "pending_amount": payment.pending_amount,
            "payment_method": payment.payment_method
        }
        payment.receipt_path = generate_payment_receipt_pdf(receipt_meta)
        db.commit()

    abs_path = os.path.join(settings.UPLOAD_DIR, payment.receipt_path.replace("/uploads/", ""))
    if not os.path.exists(abs_path):
        raise HTTPException(status_code=404, detail="Receipt file not found on disk.")

    return FileResponse(abs_path, media_type="application/pdf", filename=f"Receipt_{payment.transaction_reference}.pdf")
