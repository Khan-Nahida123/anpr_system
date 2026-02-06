"""
cropper.py
----------
Cropping helper functions for ANPR pipeline.

Why needed?
- After YOLO returns bbox, we crop that region for OCR.
- If YOLO bbox is None (generic model / missed detection), we use a fallback
  center crop to still extract plate text.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
import numpy as np


# ------------------------------------------------------------
# 1) Crop using YOLO bbox
# ------------------------------------------------------------
def crop_bbox(image_bgr: np.ndarray, bbox):
    """
    Crop an OpenCV image using bbox coordinates.

    Args:
        image_bgr: OpenCV image in BGR format (numpy array)
        bbox: list/tuple [x1, y1, x2, y2] in pixel coordinates

    Returns:
        Cropped BGR image (numpy array) if bbox is valid,
        otherwise None.
    """
    # If detection failed, nothing to crop
    if bbox is None:
        return None

    h, w = image_bgr.shape[:2]
    x1, y1, x2, y2 = bbox

    # Clamp bbox values within image boundaries
    # This avoids index errors if bbox goes out of frame
    x1 = max(0, min(x1, w - 1))
    x2 = max(0, min(x2, w - 1))
    y1 = max(0, min(y1, h - 1))
    y2 = max(0, min(y2, h - 1))

    # Invalid bbox (no area)
    if x2 <= x1 or y2 <= y1:
        return None

    # Crop and return a copy (safe for later processing)
    return image_bgr[y1:y2, x1:x2].copy()


# ------------------------------------------------------------
# 2) Fallback center crop (when bbox is missing)
# ------------------------------------------------------------
def crop_center_region(image_bgr: np.ndarray, width_ratio=0.85, height_ratio=0.45):
    """
    Fallback crop when YOLO bbox is None.

    Strategy:
    - Take a big region around the center where plates typically appear.

    Args:
        image_bgr: OpenCV image in BGR format
        width_ratio: fraction of width to keep (0-1)
        height_ratio: fraction of height to keep (0-1)

    Returns:
        Center-cropped BGR image (numpy array).
    """
    h, w = image_bgr.shape[:2]

    # Compute crop dimensions
    cw = int(w * width_ratio)
    ch = int(h * height_ratio)

    # Compute centered bounding rectangle
    x1 = max(0, (w - cw) // 2)
    y1 = max(0, (h - ch) // 2)
    x2 = min(w, x1 + cw)
    y2 = min(h, y1 + ch)

    return image_bgr[y1:y2, x1:x2].copy()
