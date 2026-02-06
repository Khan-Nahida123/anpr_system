"""
detector.py
-----------
YOLO-based number plate detector.

Purpose:
- Load a YOLO model (Ultralytics)
- Run inference on an OpenCV image (BGR numpy array)
- Return the most confident bounding box for the plate

Note:
- Currently using "yolov8n.pt" (generic model) for pipeline testing.
- Final version should use trained plate weights, e.g. "models/best.pt".
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
from ultralytics import YOLO
import numpy as np


# ------------------------------------------------------------
# PlateDetector (YOLO Wrapper)
# ------------------------------------------------------------
class PlateDetector:
    """
    Wrapper around Ultralytics YOLO model.

    Exposes:
    - detect_best_plate(image_bgr): returns the most confident bbox + confidence.
    """

    def __init__(self, weights_path: str):
        """
        Initialize detector by loading YOLO weights once.

        Args:
            weights_path: YOLO weights file/path.
                          Examples:
                          - "yolov8n.pt" (generic testing)
                          - "models/best.pt" (trained plate detector)
        """
        # Load YOLO model once at startup (efficient for repeated API calls)
        self.model = YOLO(weights_path)

    # ------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------
    def detect_best_plate(self, image_bgr: np.ndarray):
        """
        Run YOLO detection and return best (highest-confidence) bbox.

        Args:
            image_bgr: OpenCV image in BGR format (numpy array)

        Returns:
            bbox: [x1, y1, x2, y2] as ints (pixel coordinates), or None
            conf: float confidence score, or None

        Notes:
        - If no detections are found, returns (None, None).
        - Output bbox is in xyxy format (top-left and bottom-right).
        """
        # Run inference (verbose=False keeps logs clean)
        results = self.model(image_bgr, verbose=False)
        r = results[0]  # first image result

        # If YOLO found no boxes, return None
        if r.boxes is None or len(r.boxes) == 0:
            return None, None

        # Extract confidences and pick the best detection
        confs = r.boxes.conf.cpu().numpy()
        best_idx = int(np.argmax(confs))

        # xyxy format -> [x1, y1, x2, y2]
        box = r.boxes.xyxy[best_idx].cpu().numpy()  # shape (4,)
        conf = float(confs[best_idx])

        # Convert to plain ints (safe for JSON + cropping)
        bbox = [int(box[0]), int(box[1]), int(box[2]), int(box[3])]
        return bbox, conf
