import os
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.models import User
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/files", tags=["File Storage & Delivery"])

@router.get("/download")
def download_private_file(
    path: str = Query(..., description="Relative file path under uploads"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Authenticated file delivery endpoint.
    Verifies user authentication, prevents directory traversal, and either redirects to
    a signed S3 presigned URL or streams the file directly from local storage.
    """
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
        s3_key = path.lstrip("/")
        try:
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.S3_BUCKET, "Key": s3_key},
                ExpiresIn=3600
            )
            return RedirectResponse(url=presigned_url, status_code=307)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate secure S3 presigned URL: {str(e)}")

    # 2. Local storage branch with strict path traversal prevention
    # Strip leading slash or prefix
    clean_subpath = path.replace("/uploads/", "").lstrip("/\\")
    safe_path = os.path.normpath(os.path.join(settings.UPLOAD_DIR, clean_subpath))
    
    # Path traversal guard
    if not safe_path.startswith(os.path.abspath(settings.UPLOAD_DIR)):
        raise HTTPException(status_code=403, detail="Access denied: Directory traversal detected.")

    if not os.path.exists(safe_path) or not os.path.isfile(safe_path):
        raise HTTPException(status_code=404, detail="File not found.")

    filename = os.path.basename(safe_path)
    return FileResponse(
        safe_path,
        filename=filename,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
