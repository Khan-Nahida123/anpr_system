"""
ocr.py
------
OCR helper using EasyOCR.

Purpose:
- Extract number plate text from a (cropped/preprocessed) image.
- Return the best text with confidence score.

Why EasyOCR?
- Works well out of the box for many plate styles.
- Deep learning based OCR (PyTorch internally).
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
import re
import numpy as np
import easyocr


# ------------------------------------------------------------
# Global OCR Reader (initialized once)
# ------------------------------------------------------------
# Loading OCR models repeatedly is slow, so we create the reader once
# and reuse it for every API call.
_READER = easyocr.Reader(["en"], gpu=False)


# ------------------------------------------------------------
# 1) Text Cleaning Utility
# ------------------------------------------------------------
def clean_plate_text(text: str) -> str:
    """
    Clean OCR output text.

    Steps:
    - Convert to uppercase
    - Remove all non-alphanumeric characters

    Example:
      " 22 BH-6517 A " -> "22BH6517A"

    Args:
        text: raw OCR output string

    Returns:
        Cleaned plate string (A-Z, 0-9 only). Returns "" if input is empty.
    """
    if not text:
        return ""
    text = text.upper()
    text = re.sub(r"[^A-Z0-9]", "", text)
    return text


# ------------------------------------------------------------
# 2) OCR Function (EasyOCR)
# ------------------------------------------------------------
def ocr_easyocr(image_bgr: np.ndarray):
    """
    Run EasyOCR on the given image and return best text & confidence.

    Args:
        image_bgr: OpenCV image (BGR) or thresholded BGR image

    Returns:
        (text, conf)
        - text: cleaned OCR text (string), or "" if nothing found
        - conf: float confidence, or None if nothing found
    """
    # Run OCR inference
    results = _READER.readtext(image_bgr)

    # No text detected
    if not results:
        return "", None

    # Each result format:
    # (bbox_points, detected_text, confidence_score)
    # Choose the highest-confidence prediction
    best = max(results, key=lambda x: x[2])

    # Clean the detected text and return confidence
    text = clean_plate_text(best[1])
    conf = float(best[2])

    return text, conf
