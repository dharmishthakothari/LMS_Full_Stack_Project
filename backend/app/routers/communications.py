from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Notification, Announcement, User, Batch, Enrollment
from app.schemas.shared import NotificationResponse, AnnouncementResponse, AnnouncementCreate
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(tags=["Communications"])

# Notifications
@router.get("/api/notifications", response_model=List[NotificationResponse])
def get_user_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.id.desc()).limit(30).all()

@router.put("/api/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found.")
    
    notif.is_read = True
    db.commit()
    return {"message": "Notification marked as read."}

@router.put("/api/notifications/read-all")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.query(Notification).filter(Notification.user_id == current_user.id).update({"is_read": True})
    db.commit()
    return {"message": "All notifications marked as read."}

# Announcements
@router.get("/api/announcements", response_model=List[AnnouncementResponse])
def get_announcements(
    batch_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role = current_user.role.name
    query = db.query(Announcement)

    if role == "student" and current_user.student_profile:
        enrolled_batches = db.query(Enrollment.batch_id).filter(
            Enrollment.student_id == current_user.student_profile.id,
            Enrollment.status == "active"
        ).all()
        b_ids = [b[0] for b in enrolled_batches]
        query = query.filter(
            (Announcement.target_role.in_(["all", "student"])) |
            (Announcement.target_batch_id.in_(b_ids))
        )
    elif role == "instructor" and current_user.instructor_profile:
        inst_batches = db.query(Batch.id).filter(Batch.instructor_id == current_user.instructor_profile.id).all()
        b_ids = [b[0] for b in inst_batches]
        query = query.filter(
            (Announcement.target_role.in_(["all", "instructor"])) |
            (Announcement.target_batch_id.in_(b_ids))
        )

    if batch_id:
        query = query.filter(Announcement.target_batch_id == batch_id)

    announcements = query.order_by(Announcement.id.desc()).all()
    results = []
    for a in announcements:
        results.append({
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "target_role": a.target_role,
            "target_batch_id": a.target_batch_id,
            "batch_name": a.batch.name if a.batch else None,
            "created_at": a.created_at
        })
    return results

@router.post("/api/announcements", response_model=AnnouncementResponse)
def create_announcement(
    data: AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    ann = Announcement(
        title=data.title,
        content=data.content,
        target_role=data.target_role,
        target_batch_id=data.target_batch_id,
        published_by_id=current_user.id
    )
    db.add(ann)
    db.commit()
    db.refresh(ann)
    return {
        "id": ann.id,
        "title": ann.title,
        "content": ann.content,
        "target_role": ann.target_role,
        "target_batch_id": ann.target_batch_id,
        "batch_name": ann.batch.name if ann.batch else None,
        "created_at": ann.created_at
    }
