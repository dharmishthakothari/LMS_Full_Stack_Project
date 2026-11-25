import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from app.config import settings

def ensure_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def generate_payment_receipt_pdf(payment_data: dict) -> str:
    """Generates official LMS Fee Payment Receipt PDF"""
    receipt_dir = os.path.join(settings.UPLOAD_DIR, "receipts")
    ensure_directory(receipt_dir)
    filename = f"receipt_{payment_data['transaction_reference']}.pdf"
    filepath = os.path.join(receipt_dir, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # Header Banner
    c.setFillColor(colors.HexColor("#1E3A8A")) # Deep Blue
    c.rect(0, height - 100, width, 100, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(40, height - 55, "ACADEMIC TRAINING INSTITUTE")
    c.setFont("Helvetica", 12)
    c.drawString(40, height - 75, "Official Fee Payment Receipt")

    # Receipt Meta Details
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(400, height - 130, f"Receipt Ref: {payment_data['transaction_reference']}")
    c.drawString(400, height - 145, f"Date: {payment_data.get('payment_date', datetime.utcnow().strftime('%Y-%m-%d'))}")
    c.drawString(400, height - 160, f"Payment Mode: {payment_data.get('payment_method', 'Online')}")

    # Student Info Box
    c.setFillColor(colors.HexColor("#F3F4F6"))
    c.rect(40, height - 230, 320, 80, fill=True, stroke=False)
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height - 170, "Billed To:")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 190, f"Student Name: {payment_data['student_name']}")
    c.drawString(50, height - 205, f"Student ID: STU-{payment_data['student_id']:04d}")
    c.drawString(50, height - 220, f"Course: {payment_data['course_title']}")

    # Table Header
    y = height - 280
    c.setFillColor(colors.HexColor("#3B82F6"))
    c.rect(40, y, width - 80, 25, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y + 7, "Description")
    c.drawRightString(width - 50, y + 7, "Amount (INR)")

    # Table Row
    y -= 30
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Tuition Fee - {payment_data['course_title']}")
    c.drawRightString(width - 50, y, f"INR {float(payment_data['paid_amount']):,.2f}")

    # Separator Line
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.line(40, y - 15, width - 40, y - 15)

    # Financial Summary
    y -= 45
    c.setFont("Helvetica-Bold", 10)
    c.drawString(320, y, "Total Course Fee:")
    c.drawRightString(width - 50, y, f"INR {float(payment_data['total_fee']):,.2f}")

    y -= 20
    c.drawString(320, y, "Amount Paid this Transaction:")
    c.setFillColor(colors.HexColor("#059669")) # Emerald Green
    c.drawRightString(width - 50, y, f"INR {float(payment_data['paid_amount']):,.2f}")

    y -= 20
    c.setFillColor(colors.HexColor("#DC2626")) # Red if pending
    c.drawString(320, y, "Remaining Pending Balance:")
    c.drawRightString(width - 50, y, f"INR {float(payment_data['pending_amount']):,.2f}")

    # Footer
    c.setFillColor(colors.HexColor("#6B7280"))
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(40, 50, "This is a computer-generated receipt and requires no physical signature.")
    c.drawString(40, 35, "All payments are subject to institute fee refund and academic terms.")

    c.save()
    return f"/uploads/receipts/{filename}"


def generate_certificate_pdf(cert_data: dict) -> str:
    """Generates official High-Resolution Certificate of Course Completion"""
    cert_dir = os.path.join(settings.UPLOAD_DIR, "certificates")
    ensure_directory(cert_dir)
    filename = f"{cert_data['certificate_number']}.pdf"
    filepath = os.path.join(cert_dir, filename)

    # Landscape letter format
    c = canvas.Canvas(filepath, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Double Border Decoration
    c.setStrokeColor(colors.HexColor("#1E3A8A"))
    c.setLineWidth(4)
    c.rect(20, 20, width - 40, height - 40)

    c.setStrokeColor(colors.HexColor("#D97706")) # Gold accent
    c.setLineWidth(1.5)
    c.rect(26, 26, width - 52, height - 52)

    # Institute Title
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2.0, height - 90, "INSTITUTE OF ADVANCED TECHNOLOGIES")

    c.setFillColor(colors.HexColor("#D97706"))
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2.0, height - 115, "EXCELLENCE IN PROFESSIONAL HIGHER EDUCATION")

    # Certificate Headline
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2.0, height - 170, "CERTIFICATE OF COMPLETION")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2.0, height - 205, "This is proudly presented to")

    # Student Name
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2.0, height - 245, cert_data['student_name'].upper())

    # Text Body
    c.setFillColor(colors.HexColor("#374151"))
    c.setFont("Helvetica", 13)
    c.drawCentredString(width / 2.0, height - 280, "for successfully fulfilling all curriculum requirements, assessments, and practical projects for")

    # Course Name
    c.setFillColor(colors.HexColor("#111827"))
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2.0, height - 315, cert_data['course_title'])

    # Issue Date & Signatures
    y_sig = 90
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#1F2937"))
    c.drawString(80, y_sig, f"Issued Date: {cert_data.get('issue_date', datetime.utcnow().strftime('%Y-%m-%d'))}")
    c.drawString(80, y_sig - 15, f"Certificate ID: {cert_data['certificate_number']}")
    c.drawString(80, y_sig - 30, f"Verification ID: {cert_data['verification_id']}")

    # Signatures lines
    c.setStrokeColor(colors.HexColor("#9CA3AF"))
    c.line(width - 260, y_sig + 15, width - 80, y_sig + 15)
    c.drawCentredString(width - 170, y_sig, "Academic Director")
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width - 170, y_sig - 15, "Authorized Seal & Signature")

    c.save()
    return f"/uploads/certificates/{filename}"
