#  ANPR Traffic Violation Detection System

An end-to-end Automatic Number Plate Recognition (ANPR) system that detects vehicle license plates from images, extracts plate text using OCR, applies traffic violation rules, logs events into a database, and automatically sends fine notification emails.

This project demonstrates a production-style ML + backend + automation pipeline similar to real-world smart traffic enforcement systems.

---

##  Problem Statement

Manual traffic monitoring is slow, error-prone, and difficult to scale.

This project simulates an automated system that:

- Detects vehicle plates
- Reads text using OCR
- Applies violation rules
- Logs records into a database
- Sends automated fine notifications

The goal is to build a **complete ML system**, not just a model.

---

##  System Architecture

```
Image Upload
     ↓
YOLOv8 Plate Detection
     ↓
OCR Text Extraction
     ↓
Violation Decision Engine
     ↓
Database Logging
     ↓
Automatic Email Notification
```

Each module is isolated and modular, allowing independent scaling.

---

##  Features

- YOLOv8 license plate detection
- OCR plate text recognition
- Rule-based fine engine
- FastAPI backend API
- Streamlit demo interface
- MySQL database logging
- Automated email notifications
- Model performance reporting
- End-to-end pipeline integration

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

### 1. Clone repository

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

##  Run Backend API

```
uvicorn app.api.main:app --reload
```

API available at:

```
http://127.0.0.1:8000
```

---

##  Run Demo UI

```
streamlit run app/ui/streamlit_app.py
```

Upload image → detection → fine → email notification

---

##  Model Performance

See report:

```
reports/ANPR_Model_Report.pdf
```

Includes:

- mAP metrics
- Confusion matrix
- Precision–Recall curve
- Training loss graph

---

##  Email Demo Mode

All detected violations automatically send a fine notice to the configured demo email.

---

##  Use Case

Smart traffic enforcement system for:

- Helmet violation
- Signal jumping
- Wrong parking
- Seatbelt detection
- Overspeeding

---

##  Future Improvements

- Real-time CCTV integration
- Multi-vehicle tracking
- Cloud deployment
- Payment gateway integration
- Mobile app support

---

##  Author

ANPR Project — Machine Learning + Backend Integration Demo

---

##  Key Learning Outcomes

- End-to-end ML pipeline design
- Detection + OCR integration
- Backend API engineering
- Database automation
- System architecture thinking
- Production-style ML deployment

---
