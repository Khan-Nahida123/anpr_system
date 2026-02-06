"""
preprocess.py
-------------
Preprocessing utilities for OCR.

Goal:
Number plates often have:
- Low contrast text
- Motion blur / noise
- Extra symbols (like 'IND' strip)

This file contains:
1) preprocess_for_ocr: improve readability using grayscale + upscale + threshold
2) remove_left_strip: remove the left side 'IND' / logo region that confuses OCR
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
import cv2
import numpy as np


# ------------------------------------------------------------
# 1) OCR Preprocessing
# ------------------------------------------------------------
def preprocess_for_ocr(image_bgr: np.ndarray) -> np.ndarray:
    """
    Improve image for OCR by enhancing contrast and removing noise.

    Steps:
    1) Convert BGR -> grayscale
    2) Upscale 2x (OCR performs better on larger text)
    3) Light Gaussian blur (reduce noise)
    4) Adaptive threshold (handles different lighting conditions)
    5) Convert back to BGR (EasyOCR can read BGR images easily)

    Args:
        image_bgr: OpenCV image in BGR format

    Returns:
        BGR image after thresholding (OCR-friendly)
    """
    # Convert to grayscale (text extraction becomes easier)
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Upscale: improves OCR accuracy when characters are small
    gray = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

    # Denoise: smooth small noise without destroying edges too much
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Adaptive threshold: converts to high-contrast black/white
    th = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    # Convert back to BGR (some OCR libs expect 3 channels)
    return cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)


# ------------------------------------------------------------
# 2) Remove "IND" / Logo Strip
# ------------------------------------------------------------
def remove_left_strip(image_bgr: np.ndarray, strip_ratio: float = 0.18) -> np.ndarray:
    """
    Remove the left strip of the number plate where 'IND' + logo usually appears.

    Why?
    Many Indian plates have a vertical "IND" badge that OCR reads as text,
    causing wrong outputs ("IND") instead of the plate number.

    Args:
        image_bgr: plate-like cropped image (BGR)
        strip_ratio: fraction of width to cut from left side (0-1)

    Returns:
        Cropped BGR image with left strip removed.
    """
    h, w = image_bgr.shape[:2]
    x1 = int(w * strip_ratio)
    return image_bgr[:, x1:].copy()
