from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Role
from app.schemas.auth import LoginRequest, Token, ChangePasswordRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.schemas.user import UserResponse
from app.utils.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.dependencies.auth import get_current_user
from app.middleware.rate_limit import rate_limit_auth
from app.services.email_service import send_password_reset_email

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=Token, dependencies=[Depends(rate_limit_auth)])
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account has been deactivated. Please contact support."
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.name}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/change-password")
def change_password(
    req: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(req.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password does not match.")
    if len(req.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters.")
    
    current_user.password_hash = get_password_hash(req.new_password)
    db.commit()
    return {"message": "Password updated successfully."}

@router.post("/forgot-password", dependencies=[Depends(rate_limit_auth)])
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    # Generate a short-lived reset token if user exists (never leak user existence in response message)
    if user and user.is_active:
        token = create_access_token(
            data={"sub": str(user.id), "purpose": "password_reset"},
            expires_delta=timedelta(minutes=30)
        )
        full_name = f"{user.first_name} {user.last_name}".strip() or "User"
        send_password_reset_email(to_email=user.email, reset_token=token, recipient_name=full_name)
    return {"message": "If this email is registered, a password reset link has been dispatched."}

@router.post("/reset-password", dependencies=[Depends(rate_limit_auth)])
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    payload = decode_access_token(req.token)
    if not payload or payload.get("purpose") != "password_reset" or not payload.get("sub"):
        raise HTTPException(status_code=400, detail="Invalid or expired password reset token.")
    if len(req.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters.")

    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User account not found or inactive.")

    user.password_hash = get_password_hash(req.new_password)
    db.commit()
    return {"message": "Password reset token validated. Password updated."}

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out."}
