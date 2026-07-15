"""
Thin wrapper around Paystack's transaction API.

Needs PAYSTACK_SECRET_KEY set as an environment variable — never hardcode
it in this file. Get test keys free at https://dashboard.paystack.com
(Settings -> API Keys & Webhooks) — test keys work immediately, no
approval wait, and let you run the full flow with fake card numbers.
"""

import os
import requests

PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY", "")
PAYSTACK_BASE_URL = "https://api.paystack.co"


class PaystackError(Exception):
    pass


def _headers():
    if not PAYSTACK_SECRET_KEY:
        raise PaystackError(
            "PAYSTACK_SECRET_KEY is not set. Add it to your .env file "
            "(see .env.example) or export it before running the app."
        )
    return {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }


def initialize_transaction(email, amount_naira, reference, callback_url, metadata=None):
    """
    Starts a Paystack transaction. Amount must be converted to kobo
    (Paystack's smallest currency unit) — 1 Naira = 100 kobo.
    Returns the Paystack response dict, which includes
    data.authorization_url to redirect the customer to.
    """
    url = f"{PAYSTACK_BASE_URL}/transaction/initialize"
    payload = {
        "email": email,
        "amount": int(round(amount_naira * 100)),
        "reference": reference,
        "callback_url": callback_url,
        "currency": "NGN",
    }
    if metadata:
        payload["metadata"] = metadata

    response = requests.post(url, json=payload, headers=_headers(), timeout=15)
    data = response.json()
    if not response.ok or not data.get("status"):
        raise PaystackError(data.get("message", "Failed to initialize transaction"))
    return data


def verify_transaction(reference):
    """
    Confirms whether a transaction actually succeeded. Always verify
    server-side before treating an order as paid — never trust the
    client-side redirect alone, since URLs can be visited or replayed
    without a real payment happening.
    """
    url = f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}"
    response = requests.get(url, headers=_headers(), timeout=15)
    data = response.json()
    if not response.ok or not data.get("status"):
        raise PaystackError(data.get("message", "Failed to verify transaction"))
    return data
