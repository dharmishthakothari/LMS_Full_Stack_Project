import os
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config import settings

# Import all routers
from app.routers import (
    auth, users, students, instructors, courses,
    modules, batches, lectures, assignments,
    submissions, quizzes, attendance, progress,
    certificates, payments, communications,
    reports, health
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Full Stack Learning Management System (LMS) REST API with Role-Based Access Control.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for uploads (receipts, certificates, materials)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include Routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(students.router)
app.include_router(instructors.router)
app.include_router(courses.router)
app.include_router(modules.router)
app.include_router(batches.router)
app.include_router(lectures.router)
app.include_router(assignments.router)
app.include_router(submissions.router)
app.include_router(quizzes.router)
app.include_router(attendance.router)
app.include_router(progress.router)
app.include_router(certificates.router)
app.include_router(payments.router)
app.include_router(communications.router)
app.include_router(reports.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "message": "Input validation error"},
    )

@app.get("/")
def root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
