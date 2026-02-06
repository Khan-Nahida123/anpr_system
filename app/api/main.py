"""
ANPR FastAPI Backend
====================

End-to-end Automatic Number Plate Recognition API.

Pipeline:
Upload image → Plate detection → OCR → Fine computation
→ Database logging → Email notification (Demo mode)

This backend simulates a real-world traffic enforcement pipeline
using a modular ML + API architecture.
"""

import os
from pathlib import Path

import numpy as np
import cv2
from fastapi import FastAPI, UploadFile, File, Form
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# Environment configuration
# ---------------------------------------------------------------------

# Load environment variables from project root .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# ---------------------------------------------------------------------
# ML pipeline imports
# ---------------------------------------------------------------------

from src.detector import PlateDetector
from src.cropper import crop_bbox, crop_center_region
from src.preprocess import preprocess_for_ocr, remove_left_strip
from src.ocr import ocr_easyocr

# ---------------------------------------------------------------------
# Business logic imports
# ---------------------------------------------------------------------

from src.db_client import DBClient
from src.fine_engine import compute_fine
from src.email_sender import send_email_smtp

# ---------------------------------------------------------------------
# FastAPI app initialization
# ---------------------------------------------------------------------

app = FastAPI(title="ANPR API")

# Load trained YOLO model
detector = PlateDetector("models/best.pt")

# Database client (used for optional logging)
db = DBClient(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "anpr_db"),
)

# Demo mode: all emails are sent to the configured SMTP user
DEMO_EMAIL = os.getenv("SMTP_USER")

# ---------------------------------------------------------------------
# Health check endpoint
# ---------------------------------------------------------------------


@app.get("/health")
def health():
    """Simple health endpoint to verify API is running."""
    return {"status": "ok"}


# ---------------------------------------------------------------------
# Main ANPR endpoint
# ---------------------------------------------------------------------


@app.post("/anpr")
async def anpr(
    file: UploadFile = File(...),
    violation_type: str = Form("No Violation"),
):
    """
    Process an uploaded vehicle image and simulate a traffic violation pipeline.

    Steps:
    1. Decode uploaded image
    2. Detect number plate using YOLO
    3. Crop and preprocess plate region
    4. Run OCR to extract text
    5. Compute violation fine
    6. Log event in database
    7. Send demo email notification

    Returns:
        JSON response with plate text, violation type, fine amount,
        and email status.
    """

    # -----------------------------------------------------------------
    # Decode image
    # -----------------------------------------------------------------

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return {"status": "fail", "reason": "Invalid image"}

    # -----------------------------------------------------------------
    # Plate detection + cropping
    # -----------------------------------------------------------------

    bbox, _ = detector.detect_best_plate(img)

    crop = crop_bbox(img, bbox)
    if crop is not None:
        plate_img = crop
    else:
        # fallback center crop if detection fails
        plate_img = crop_center_region(img, width_ratio=0.95, height_ratio=0.55)

    # Remove left strip and enhance OCR readability
    plate_img = remove_left_strip(plate_img, strip_ratio=0.18)
    plate_img_pp = preprocess_for_ocr(plate_img)

    # -----------------------------------------------------------------
    # OCR extraction
    # -----------------------------------------------------------------

    ocr_text, ocr_conf = ocr_easyocr(plate_img_pp)

    # -----------------------------------------------------------------
    # Fine computation
    # -----------------------------------------------------------------

    is_fined, fine_amount = compute_fine(violation_type)

    db_log = None
    email_result = None

    # -----------------------------------------------------------------
    # Database logging (safe mode)
    # -----------------------------------------------------------------

    if ocr_text:
        try:
            db_log = db.insert_fine_log(
                plate=ocr_text,
                violation_type=violation_type,
                fine_amount=fine_amount,
                is_fined=is_fined,
                ocr_text=ocr_text,
                ocr_conf=float(ocr_conf) if ocr_conf else None,
                email_sent=0,
            )
        except Exception as e:
            print("DB log error:", e)

    # -----------------------------------------------------------------
    # Demo email notification
    # -----------------------------------------------------------------

    if DEMO_EMAIL and ocr_text:
        subject = f"Traffic Fine Notice - Plate {ocr_text}"

        body = (
            f"Detected Plate: {ocr_text}\n"
            f"Violation: {violation_type}\n"
            f"Fine: INR {fine_amount}\n\n"
        )

        email_result = send_email_smtp(DEMO_EMAIL, subject, body)

        # Mark email sent in DB if successful
        if (
            email_result.get("sent")
            and db_log
            and isinstance(db_log, dict)
            and "fine_id" in db_log
        ):
            db.mark_email_sent(db_log["fine_id"])

    # -----------------------------------------------------------------
    # API response
    # -----------------------------------------------------------------

    return {
        "status": "success",
        "plate": ocr_text,
        "violation": violation_type,
        "fine": fine_amount,
        "email_sent": email_result.get("sent") if email_result else False
    }