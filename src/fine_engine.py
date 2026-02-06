"""
fine_engine.py
--------------
Fine calculation module (rule-based).

Purpose:
- Convert a selected violation type into:
    1) is_fined (1/0)
    2) fine_amount (INR)

Notes:
- This is a DEMO/portfolio implementation.
- In real systems, fine rules come from:
  government regulations, city/state rules, time-based conditions,
  vehicle category, repeat offenses, etc.
"""

# ------------------------------------------------------------
# Demo fine rules (INR)
# ------------------------------------------------------------
# Key = violation name (must match Streamlit dropdown)
# Value = fine amount in INR
FINE_RULES = {
    "No Helmet": 500,
    "Signal Jump": 1000,
    "Wrong Parking": 300,
    "No Seatbelt": 500,
    "Overspeeding": 1500,
    "No Violation": 0
}


def compute_fine(violation_type: str):
    """
    Compute fine for a given violation type.

    Args:
        violation_type: string selected from UI (e.g., "Signal Jump")

    Returns:
        is_fined: 1 if fine_amount > 0 else 0
        fine_amount: integer amount in INR
    """
    # Get amount from rules; default to 0 if unknown violation type
    amount = FINE_RULES.get(violation_type, 0)

    # Convert amount to a simple yes/no fine flag
    is_fined = 1 if amount > 0 else 0

    return is_fined, amount
