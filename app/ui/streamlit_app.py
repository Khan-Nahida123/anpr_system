"""
Streamlit Frontend - ANPR Demo
==============================

Interactive UI for the ANPR system.

Flow:
Upload image → Send to FastAPI → Show detection result → Email status

This UI demonstrates real-time ML inference + backend integration.
"""

import streamlit as st
import requests

# ---------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------

st.set_page_config(page_title="ANPR Demo", layout="centered")

st.title("ANPR Demo")
st.write("Upload a vehicle image → automatic plate detection + fine notification")

API_BASE = "http://127.0.0.1:8000"

# ---------------------------------------------------------------------
# Violation selector
# ---------------------------------------------------------------------

violation = st.selectbox(
    "Violation type",
    [
        "No Violation",
        "No Helmet",
        "Signal Jump",
        "Wrong Parking",
        "No Seatbelt",
        "Overspeeding",
    ],
)

# ---------------------------------------------------------------------
# Image upload
# ---------------------------------------------------------------------

uploaded = st.file_uploader(
    "Upload vehicle image",
    type=["jpg", "jpeg", "png"]
)

# ---------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------

if uploaded is not None:
    st.image(uploaded, caption="Uploaded Image", use_container_width=True)

    if st.button("Run ANPR"):

        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        data = {"violation_type": violation}

        try:
            response = requests.post(
                f"{API_BASE}/anpr",
                files=files,
                data=data,
                timeout=120
            )

            result = response.json()

            st.success("Processing complete ✅")

            # ---------------------------------------------------------
            # Result display
            # ---------------------------------------------------------

            st.write(f"**Detected Plate:** {result.get('plate')}")
            st.write(f"**Violation:** {result.get('violation')}")
            st.write(f"**Fine Amount:** ₹{result.get('fine')}")

            # ---------------------------------------------------------
            # Email status
            # ---------------------------------------------------------

            if result.get("email_sent"):
                st.success("Email notification sent 📧")
            else:
                st.warning("Email not sent")

        except Exception as e:
            st.error(f"API error: {e}")