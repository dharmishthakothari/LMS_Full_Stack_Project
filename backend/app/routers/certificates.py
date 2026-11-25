from typing import List, Optional
import os
import uuid
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.models import Certificate, Student, Course, User
from app.dependencies.auth import get_current_user, require_role
from app.services.progress_service import calculate_student_course_progress
from app.services.pdf_service import generate_certificate_pdf

router = APIRouter(prefix="/api/certificates", tags=["Certificates"])

@router.get("")
def list_certificates(
    student_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Certificate)
    if current_user.role.name == "student":
        if not current_user.student_profile:
            return []
        query = query.filter(Certificate.student_id == current_user.student_profile.id)
    elif student_id:
        query = query.filter(Certificate.student_id == student_id)

    certs = query.order_by(Certificate.id.desc()).all()
    return [
        {
            "id": c.id,
            "certificate_number": c.certificate_number,
            "verification_id": c.verification_id,
            "student_id": c.student_id,
            "student_name": f"{c.student.user.first_name} {c.student.user.last_name}",
            "course_id": c.course_id,
            "course_title": c.course.title,
            "issue_date": c.issue_date.isoformat(),
            "pdf_path": c.pdf_path
        }
        for c in certs
    ]

@router.post("/generate")
def generate_certificate(
    student_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify student identity if student
    if current_user.role.name == "student":
        if not current_user.student_profile or current_user.student_profile.id != student_id:
            raise HTTPException(status_code=403, detail="Access denied.")

    # Check existing certificate
    existing = db.query(Certificate).filter(
        Certificate.student_id == student_id,
        Certificate.course_id == course_id
    ).first()
    if existing:
        return {"message": "Certificate already generated.", "certificate_id": existing.id, "pdf_path": existing.pdf_path}

    # Verify eligibility via progress service
    progress = calculate_student_course_progress(db, student_id, course_id)
    if not progress.get("is_eligible_for_certificate"):
        raise HTTPException(
            status_code=400,
            detail="Student is not yet eligible for certificate. Requirements: Course progress >= 80%, Attendance >= 75%, and All Fees cleared."
        )

    cert_num = f"CERT-{course_id:02d}-{uuid.uuid4().hex[:6].upper()}"
    verify_id = f"V-LMS-{uuid.uuid4().hex[:8].upper()}"
    student = db.query(Student).filter(Student.id == student_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()

    cert_data = {
        "certificate_number": cert_num,
        "verification_id": verify_id,
        "student_name": f"{student.user.first_name} {student.user.last_name}",
        "course_title": course.title,
        "issue_date": date.today().isoformat()
    }
    pdf_path = generate_certificate_pdf(cert_data)

    cert = Certificate(
        certificate_number=cert_num,
        verification_id=verify_id,
        student_id=student_id,
        course_id=course_id,
        issue_date=date.today(),
        pdf_path=pdf_path
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)

    return {"message": "Certificate generated successfully.", "certificate_id": cert.id, "pdf_path": cert.pdf_path}

@router.get("/verify/{verification_id}")
def verify_certificate_public(verification_id: str, db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(Certificate.verification_id == verification_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Invalid certificate or verification ID not found.")

    return {
        "is_valid": True,
        "certificate_number": cert.certificate_number,
        "student_name": f"{cert.student.user.first_name} {cert.student.user.last_name}",
        "course_title": cert.course.title,
        "issue_date": cert.issue_date.isoformat(),
        "status": "Verified Authentic Credential",
        "issuing_institute": "Academic Training Institute"
    }

@router.get("/{certificate_id}/download")
def download_certificate_pdf(
    certificate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cert = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found.")

    if current_user.role.name == "student":
        if cert.student_id != current_user.student_profile.id:
            raise HTTPException(status_code=403, detail="Access denied.")

    abs_path = os.path.join(settings.UPLOAD_DIR, cert.pdf_path.replace("/uploads/", ""))
    if not os.path.exists(abs_path):
        # Re-generate PDF
        cert_data = {
            "certificate_number": cert.certificate_number,
            "verification_id": cert.verification_id,
            "student_name": f"{cert.student.user.first_name} {cert.student.user.last_name}",
            "course_title": cert.course.title,
            "issue_date": cert.issue_date.isoformat()
        }
        cert.pdf_path = generate_certificate_pdf(cert_data)
        db.commit()
        abs_path = os.path.join(settings.UPLOAD_DIR, cert.pdf_path.replace("/uploads/", ""))

    return FileResponse(abs_path, media_type="application/pdf", filename=f"{cert.certificate_number}.pdf")
