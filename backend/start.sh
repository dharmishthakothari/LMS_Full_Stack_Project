#!/bin/sh
set -e
echo "Initializing LMS database..."
python -c "from app.database import Base, engine; import app.models; Base.metadata.create_all(bind=engine); print('Database ready')" || true
echo "Starting Uvicorn web server on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
