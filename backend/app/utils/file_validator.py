import os
import re
import uuid
from fastapi import HTTPException, UploadFile
from app.config import settings

ALLOWED_MATERIAL_EXTENSIONS = {".pdf", ".ppt", ".pptx", ".doc", ".docx", ".txt", ".zip", ".mp4", ".webm"}
ALLOWED_SUBMISSION_EXTENSIONS = {".pdf", ".zip", ".tar", ".gz", ".doc", ".docx", ".txt", ".py", ".js", ".jsx"}

def sanitize_filename(filename: str) -> str:
    """Strip directory paths and unsafe characters from uploaded filenames."""
    base = os.path.basename(filename or "upload")
    clean = re.sub(r"[^A-Za-z0-9._-]", "_", base)
    return clean or "file"

async def validate_and_read_upload(
    file: UploadFile,
    allowed_extensions: set,
    max_mb: int = settings.MAX_UPLOAD_SIZE_MB
) -> tuple[str, bytes]:
    """Validate file extension and size before saving to storage."""
    clean_name = sanitize_filename(file.filename)
    _, ext = os.path.splitext(clean_name)
    if ext.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(allowed_extensions))}"
        )

    contents = await file.read()
    max_bytes = max_mb * 1024 * 1024
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum limit of {max_mb} MB."
        )

    safe_storage_name = f"{uuid.uuid4().hex}_{clean_name}"
    return safe_storage_name, contents
