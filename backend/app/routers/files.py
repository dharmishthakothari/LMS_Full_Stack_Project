import os
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.models import User, Submission, Certificate, Payment, StudyMaterial, Enrollment, Batch
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/files", tags=["File Storage & Delivery"])


def _authorize_file_access(db: Session, current_user: User, clean_subpath: str) -> None:
    """Enforce role-based and ownership-based access control for private files."""
    role = current_user.role.name if current_user.role else ""
    if role == "admin":
        return

    candidate_paths = {clean_subpath, f"/uploads/{clean_subpath}", f"/{clean_subpath}"}

    # 1. Check Submissions
    sub = db.query(Submission).filter(Submission.file_path.in_(candidate_paths)).first()
    if sub:
        if role == "student" and current_user.student_profile and sub.student_id == current_user.student_profile.id:
            return
        if role == "instructor" and current_user.instructor_profile and sub.assignment and sub.assignment.batch:
            if sub.assignment.batch.instructor_id == current_user.instructor_profile.id:
                return
        raise HTTPException(status_code=403, detail="Access denied: You do not have permission to access this submission.")

    # 2. Check Certificates
    cert = db.query(Certificate).filter(Certificate.pdf_path.in_(candidate_paths)).first()
    if cert:
        if role == "student" and current_user.student_profile and cert.student_id == current_user.student_profile.id:
            return
        raise HTTPException(status_code=403, detail="Access denied: You do not have permission to access this certificate.")

    # 3. Check Payment Receipts
    pay = db.query(Payment).filter(Payment.receipt_path.in_(candidate_paths)).first()
    if pay:
        if role == "student" and current_user.student_profile and pay.student_id == current_user.student_profile.id:
            return
        raise HTTPException(status_code=403, detail="Access denied: You do not have permission to access this receipt.")

    # 4. Check Study Materials
    mat = db.query(StudyMaterial).filter(StudyMaterial.file_path.in_(candidate_paths)).first()
    if mat:
        if role == "instructor":
            return
        if role == "student" and current_user.student_profile and mat.lecture and mat.lecture.module:
            course_id = mat.lecture.module.course_id
            enrolled = (
                db.query(Enrollment)
                .join(Batch)
                .filter(
                    Enrollment.student_id == current_user.student_profile.id,
                    Enrollment.status == "active",
                    Batch.course_id == course_id,
                )
                .first()
            )
            if enrolled:
                return
        raise HTTPException(status_code=403, detail="Access denied: You are not enrolled in this course.")

    # Default deny for unregistered/unowned file paths
    raise HTTPException(status_code=403, detail="Access denied: File ownership could not be verified.")


@router.get("/download")
def download_private_file(
    path: str = Query(..., description="Relative file path under uploads"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Authenticated and RBAC-scoped file delivery endpoint.
    Prevents directory traversal, verifies ownership/role permissions, and either redirects to
    a signed S3 presigned URL or streams the file directly from local storage.
    """
    clean_subpath = path.replace("/uploads/", "").lstrip("/\\")

    # Path traversal guard
    safe_path = os.path.normpath(os.path.join(settings.UPLOAD_DIR, clean_subpath))
    if not safe_path.startswith(os.path.abspath(settings.UPLOAD_DIR)):
        raise HTTPException(status_code=403, detail="Access denied: Directory traversal detected.")

    # Enforce ownership / role authorization
    _authorize_file_access(db, current_user, clean_subpath.replace("\\", "/"))

    # 1. S3 Object Storage branch
    if settings.STORAGE_BACKEND == "s3" and settings.S3_BUCKET:
        import boto3
        from botocore.config import Config
        s3_client = boto3.client(
            "s3",
            region_name=settings.S3_REGION,
            endpoint_url=settings.S3_ENDPOINT_URL or None,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID or None,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY or None,
            config=Config(signature_version="s3v4")
        )
        s3_key = clean_subpath.lstrip("/")
        try:
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.S3_BUCKET, "Key": s3_key},
                ExpiresIn=3600
            )
            return RedirectResponse(url=presigned_url, status_code=307)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate secure S3 presigned URL: {str(e)}")

    # 2. Local storage branch
    if not os.path.exists(safe_path) or not os.path.isfile(safe_path):
        raise HTTPException(status_code=404, detail="File not found.")

    filename = os.path.basename(safe_path)
    return FileResponse(
        safe_path,
        filename=filename,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
