"""
gemini_client.py
----------------
Gemini (Google GenAI) helper for drafting a fine-notice email.

Important:
- Uses the NEW official SDK: `google-genai`
- Reads GEMINI_API_KEY from .env

Behavior:
- If key missing / API fails, returns a safe fallback draft.
"""

from __future__ import annotations

import os
from typing import Any, Dict

try:
    # NEW SDK (recommended by Google)
    from google import genai
except Exception:
    genai = None


# ------------------------------------------------------------
# Fallback draft (used if Gemini fails / not configured)
# ------------------------------------------------------------
def _fallback_draft(owner_name: str, plate: str, violation: str, fine_amount: int) -> str:
    return (
        f"Dear {owner_name},\n\n"
        f"This is a notice regarding a traffic violation detected for your vehicle.\n\n"
        f"Plate Number: {plate}\n"
        f"Violation: {violation}\n"
        f"Fine Amount: INR {fine_amount}\n\n"
        f"Please pay the fine as per applicable rules.\n\n"
        f"Regards,\n"
        f"ANPR Demo System\n"
    )


# ------------------------------------------------------------
# Public function
# ------------------------------------------------------------
def draft_fine_email_with_gemini(
    owner_name: str,
    plate: str,
    violation: str,
    fine_amount: int
) -> Dict[str, Any]:
    """
    Returns:
      {
        "ok": True/False,
        "draft": "...",
        "mode": "gemini" or "fallback",
        "error": "..." or ""
      }
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    # If SDK missing or key missing -> fallback
    if (genai is None) or (not api_key):
        return {
            "ok": False,
            "draft": _fallback_draft(owner_name, plate, violation, fine_amount),
            "mode": "fallback",
            "error": "Gemini not configured (missing google-genai or GEMINI_API_KEY)."
        }

    try:
        client = genai.Client(api_key=api_key)

        prompt = (
            "You are drafting a professional traffic fine notice email.\n"
            "Write a short, clear email in English with:\n"
            "- Greeting using the owner's name\n"
            "- Plate number\n"
            "- Violation type\n"
            "- Fine amount in INR\n"
            "- One simple payment instruction line\n"
            "- Polite closing\n\n"
            "Rules:\n"
            "- Do NOT include threats.\n"
            "- Do NOT invent payment links.\n"
            "- Keep it concise.\n\n"
            f"Owner Name: {owner_name}\n"
            f"Plate Number: {plate}\n"
            f"Violation: {violation}\n"
            f"Fine Amount (INR): {fine_amount}\n"
        )

        # ✅ Model name for new SDK (works widely)
        # If you want, later you can switch to another available model.
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        draft = (getattr(resp, "text", "") or "").strip()

        if not draft:
            return {
                "ok": False,
                "draft": _fallback_draft(owner_name, plate, violation, fine_amount),
                "mode": "fallback",
                "error": "Gemini returned empty text."
            }

        return {"ok": True, "draft": draft, "mode": "gemini", "error": ""}

    except Exception as e:
        return {
            "ok": False,
            "draft": _fallback_draft(owner_name, plate, violation, fine_amount),
            "mode": "fallback",
            "error": str(e)
        }

