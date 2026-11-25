"""Storage abstraction supporting local filesystem (dev) and S3-compatible object storage (prod)."""

import os
from typing import Optional
from app.config import settings


def save_bytes(key: str, data: bytes, content_type: Optional[str] = None) -> str:
    """Save file bytes to configured storage backend and return accessible path/URL."""
    if settings.STORAGE_BACKEND.lower() == "s3" and settings.S3_BUCKET:
        import boto3

        client_kwargs = {"region_name": settings.S3_REGION}
        if settings.S3_ENDPOINT_URL:
            client_kwargs["endpoint_url"] = settings.S3_ENDPOINT_URL
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            client_kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
            client_kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY

        s3 = boto3.client("s3", **client_kwargs)
        put_kwargs = {"Bucket": settings.S3_BUCKET, "Key": key, "Body": data}
        if content_type:
            put_kwargs["ContentType"] = content_type
        s3.put_object(**put_kwargs)

        if settings.S3_PUBLIC_BASE_URL:
            return f"{settings.S3_PUBLIC_BASE_URL.rstrip('/')}/{key}"
        return f"s3://{settings.S3_BUCKET}/{key}"

    # Local filesystem fallback for development
    dest_path = os.path.join(settings.UPLOAD_DIR, key)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(data)
    return f"/uploads/{key.replace(os.sep, '/')}"
