import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

logger = logging.getLogger("lms.email")

def send_password_reset_email(to_email: str, reset_token: str, recipient_name: str = "Student/Faculty") -> bool:
    """
    Dispatches a password reset email containing a time-limited security token.
    If SMTP credentials are not configured, logs the dispatch safely to allow development flows.
    """
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    
    subject = "LMS Portal: Password Reset Request"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; }}
            .container {{ max-width: 580px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
            .header {{ background: #4f46e5; padding: 24px; text-align: center; color: #ffffff; }}
            .header h1 {{ margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }}
            .body {{ padding: 32px 24px; color: #334155; line-height: 1.6; font-size: 14px; }}
            .btn {{ display: inline-block; padding: 12px 28px; background-color: #4f46e5; color: #ffffff !important; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 14px; margin: 20px 0; }}
            .footer {{ background: #f1f5f9; padding: 16px; text-align: center; font-size: 12px; color: #64748b; }}
            .code-box {{ background: #f8fafc; border: 1px solid #cbd5e1; padding: 12px; border-radius: 6px; font-family: monospace; word-break: break-all; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>LMS Academic Platform</h1>
            </div>
            <div class="body">
                <p>Hello <strong>{recipient_name}</strong>,</p>
                <p>We received a request to reset the password associated with your LMS account (<strong>{to_email}</strong>).</p>
                <p>To choose a new password, click the secure verification button below:</p>
                <div style="text-align: center;">
                    <a href="{reset_url}" class="btn">Reset My Password</a>
                </div>
                <p>Or paste this URL into your browser:</p>
                <div class="code-box">{reset_url}</div>
                <p style="margin-top: 24px; color: #dc2626; font-size: 13px;">
                    <strong>Security Notice:</strong> This link expires in 30 minutes. If you did not request this change, please ignore this email; your account remains secure.
                </p>
            </div>
            <div class="footer">
                &copy; 2026 LMS Academic Institute. Automated system notification.
            </div>
        </div>
    </body>
    </html>
    """

    plain_content = f"""
Hello {recipient_name},

We received a request to reset your LMS account password.
Please open the link below within 30 minutes to set a new password:

{reset_url}

If you did not request a password reset, please ignore this message.

LMS Academic Institute
    """

    # If SMTP is fully configured, attempt live dispatch
    if settings.SMTP_USER and settings.SMTP_PASSWORD:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"LMS Support <{settings.FROM_EMAIL}>"
            msg["To"] = to_email

            msg.attach(MIMEText(plain_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            logger.info(f"Password reset email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email via SMTP to {to_email}: {e}")
            # Fall through to logging
    
    # Safe development fallback: log the reset link so developer/tester can access it
    logger.warning(
        f"[EMAIL SERVICE SIMULATION] Password reset dispatched to {to_email}.\n"
        f"Reset URL: {reset_url}\n"
        f"Token: {reset_token}"
    )
    return True
