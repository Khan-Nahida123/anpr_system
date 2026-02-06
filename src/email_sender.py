"""
email_sender.py
---------------
SMTP email sending helper.

Security:
- Credentials are loaded from .env (never hardcode).
"""

from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage
load_dotenv()


def send_email_smtp(to_email: str, subject: str, body: str) -> dict:
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_pass = os.getenv("SMTP_PASS", "").strip()

    #  DEBUG PRINTS
    print("SMTP user:", smtp_user)
    print("Sending to:", to_email)

    if not smtp_user or not smtp_pass:
        print("❌ SMTP credentials missing")
        return {"sent": False, "error": "SMTP credentials missing (check .env)"}

    try:
        msg = EmailMessage()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        print("✅ Email sent successfully")
        return {"sent": True}

    except Exception as e:
        print("❌ Email error:", e)
        return {"sent": False, "error": str(e)}


# --------------------------------------------------
#  TEMP TEST EMAIL (delete after testing)
# --------------------------------------------------
if __name__ == "__main__":
    send_email_smtp(
        "nahidak724@gmail.com",   # ← apna email yahan likho
        "SMTP Test",
        "Hello from ANPR system"
    )
