#  ANPR Traffic Violation System

Automatic Number Plate Recognition (ANPR) system that detects vehicle plates from images, extracts text using OCR, applies traffic violation rules, logs to database, and automatically sends fine notifications via email.

This project demonstrates an end-to-end ML + Backend + UI pipeline.

---

##  Features

- YOLOv8 license plate detection
- OCR plate text extraction
- Traffic fine rule engine
- FastAPI backend API
- Streamlit demo UI
- MySQL database logging
- Automatic email notification
- Model performance report generation

---

##  Tech Stack

- Python
- YOLOv8 (Ultralytics)
- EasyOCR
- OpenCV
- FastAPI
- Streamlit
- MySQL
- SMTP Email
- Matplotlib / Seaborn

---

##  Project Structure

```
app/        → FastAPI backend
src/        → ML pipeline modules
models/     → Trained YOLO model
db/         → Database schema & seed
notebooks/  → Training notebook
reports/    → Model performance report
```

---

##  Setup Instructions

### 1. Clone repo

```
git clone <your_repo_link>
cd anpr-project
```

### 2. Create virtual environment

```
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure environment

Create `.env` file:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=anpr_db

SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

---

##  Run Backend

```
uvicorn app.main:app --reload
```

API runs at:

```
http://127.0.0.1:8000
```

---

##  Run UI Demo

```
streamlit run app/ui.py
```

Upload image → detection → email fine

---

##  Model Performance

See `reports/ANPR_Model_Report.pdf`

Includes:

- mAP metrics
- Confusion matrix
- Precision-Recall curve
- Training loss

---

##  Email Demo Mode

All fines are sent to demo email configured in `.env`.

---

##  Use Case

Smart traffic enforcement system for:

- Helmet violation
- Signal jumping
- Wrong parking
- Seatbelt detection
- Overspeeding

---

##  Author

ANPR Project — Machine Learning + Backend Integration Demo

---

##  Future Improvements

- Real-time CCTV integration
- Mobile deployment
- Multi-vehicle tracking
- Cloud hosting
- Payment gateway integration

---

