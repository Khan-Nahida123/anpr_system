"""
db_client.py
------------
MySQL helper module for ANPR project.

Responsibilities:
1) Fetch owner + vehicle info by plate number
2) Insert fine logs after processing
3) Mark email as sent (email_sent = 1)

Ethics note:
- This project uses DEMO / mock owner data stored locally.
- No real personal data is used.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
import mysql.connector
from mysql.connector import Error


# ------------------------------------------------------------
# DB Client Wrapper
# ------------------------------------------------------------
class DBClient:
    """
    Small database wrapper to keep API code clean.
    """

    # ------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------
    def __init__(self, host="localhost", user="root", password="", database="anpr_db"):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }

    # ------------------------------------------------------------
    # Internal Connection Helper
    # ------------------------------------------------------------
    def _connect(self):
        return mysql.connector.connect(**self.config)

    # ------------------------------------------------------------
    # 1) Owner Lookup by Plate
    # ------------------------------------------------------------
    def get_owner_by_plate(self, plate: str):
        query = """
        SELECT v.plate_number, o.name, o.email, o.phone, v.vehicle_type
        FROM vehicles v
        JOIN owners o ON v.owner_id = o.owner_id
        WHERE v.plate_number = %s
        """
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute(query, (plate,))
            row = cur.fetchone()

            cur.close()
            conn.close()

            if not row:
                return None

            return {
                "plate_number": row[0],
                "owner_name": row[1],
                "email": row[2],
                "phone": row[3],
                "vehicle_type": row[4],
            }

        except Error as e:
            return {"error": str(e)}

    # ------------------------------------------------------------
    # 2) Fine Log Insert
    # ------------------------------------------------------------
    def insert_fine_log(
        self,
        plate: str,
        violation_type: str,
        fine_amount: int,
        is_fined: int,
        ocr_text: str,
        ocr_conf: float,
        email_sent: int = 0
    ):
        query = """
        INSERT INTO fines (plate_number, violation_type, fine_amount, is_fined, ocr_text, ocr_conf, email_sent)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute(
                query,
                (plate, violation_type, fine_amount, is_fined, ocr_text, ocr_conf, email_sent)
            )
            conn.commit()

            fine_id = cur.lastrowid

            cur.close()
            conn.close()

            return {"fine_id": fine_id}

        except Error as e:
            return {"error": str(e)}

    # ------------------------------------------------------------
    # 3) Mark Email Sent
    # ------------------------------------------------------------
    def mark_email_sent(self, fine_id: int):
        query = "UPDATE fines SET email_sent = 1 WHERE fine_id = %s"
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute(query, (fine_id,))
            conn.commit()

            cur.close()
            conn.close()

            return {"updated": True}

        except Error as e:
            return {"error": str(e)}
