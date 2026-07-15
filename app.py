"""
VMAX Tea & Coffee Shop — Flask web app with cart + Paystack checkout.

Setup:
    1. cp .env.example .env
    2. Fill in PAYSTACK_SECRET_KEY and PAYSTACK_PUBLIC_KEY (test keys
       from https://dashboard.paystack.com/#/settings/developer)
    3. pip install -r requirements.txt
    4. python app.py
"""

import os
import uuid

from flask import Flask, render_template, jsonify, redirect, request, url_for, flash
from dotenv import load_dotenv

import cart
from menu import MENU_ITEMS, CATEGORIES, items_by_category, get_item
from paystack import initialize_transaction, verify_transaction, PaystackError

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-this")

# Verified business info — single source of truth, used across templates.
BUSINESS = {
    "name": "VMAX Tea And Coffee Shop",
    "address": "Enipaul Plaza, 253 Oron Road, Opposite Winners Chapel, Uyo 520101, Akwa Ibom, Nigeria",
    "phone": "+2348069924218",
    "phone_display": "+234 806 992 4218",
    "rating": 5.0,
    "hours": {
        "Monday": "8:30 AM – 9:00 PM",
        "Tuesday": "8:30 AM – 9:00 PM",
        "Wednesday": "8:30 AM – 9:00 PM",
        "Thursday": "8:00 AM – 9:00 PM",
        "Friday": "8:00 AM – 9:00 PM",
        "Saturday": "8:00 AM – 9:00 PM",
        "Sunday": "8:00 AM – 9:00 PM",
    },
}


@app.route("/")
def home():
    return render_template(
        "index.html",
        business=BUSINESS,
        categories=CATEGORIES,
        menu_items=MENU_ITEMS,
        cart_count=cart.item_count(),
    )


# ---------- Cart ----------

@app.route("/cart/add", methods=["POST"])
def cart_add():
    item_id = request.form.get("item_id")
    quantity = int(request.form.get("quantity", 1))
    ok = cart.add(item_id, quantity)
    if request.headers.get("Accept") == "application/json":
        return jsonify(success=ok, cart_count=cart.item_count())
    if not ok:
        flash("That item couldn't be found.", "error")
    return redirect(request.referrer or url_for("home"))


@app.route("/cart/update", methods=["POST"])
def cart_update():
    item_id = request.form.get("item_id")
    quantity = int(request.form.get("quantity", 1))
    cart.set_quantity(item_id, quantity)
    return redirect(url_for("cart_view"))


@app.route("/cart/remove", methods=["POST"])
def cart_remove():
    item_id = request.form.get("item_id")
    cart.remove(item_id)
    return redirect(url_for("cart_view"))


@app.route("/cart")
def cart_view():
    return render_template(
        "cart.html",
        business=BUSINESS,
        lines=cart.contents(),
        total=cart.total(),
        cart_count=cart.item_count(),
    )


# ---------- Checkout ----------

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    lines = cart.contents()
    if not lines:
        flash("Your cart is empty.", "error")
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template(
            "checkout.html",
            business=BUSINESS,
            lines=lines,
            total=cart.total(),
            cart_count=cart.item_count(),
        )

    # POST: customer submitted the checkout form — start a Paystack transaction
    email = request.form.get("email", "").strip()
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()

    if not email:
        flash("An email is required to receive your receipt.", "error")
        return redirect(url_for("checkout"))

    reference = f"vmax_{uuid.uuid4().hex[:12]}"

    try:
        result = initialize_transaction(
            email=email,
            amount_naira=cart.total(),
            reference=reference,
            callback_url=url_for("checkout_callback", _external=True),
            metadata={
                "customer_name": name,
                "customer_phone": phone,
                "cart_summary": [
                    {"name": line["item"]["name"], "qty": line["quantity"]}
                    for line in lines
                ],
            },
        )
    except PaystackError as e:
        flash(f"Couldn't start checkout: {e}", "error")
        return redirect(url_for("checkout"))

    return redirect(result["data"]["authorization_url"])


@app.route("/checkout/callback")
def checkout_callback():
    reference = request.args.get("reference") or request.args.get("trxref")
    if not reference:
        flash("Missing payment reference.", "error")
        return redirect(url_for("home"))

    try:
        result = verify_transaction(reference)
    except PaystackError as e:
        flash(f"Couldn't verify payment: {e}", "error")
        return redirect(url_for("home"))

    data = result.get("data", {})
    paid = data.get("status") == "success"

    if paid:
        order_summary = cart.contents()
        order_total = cart.total()
        cart.clear()
        return render_template(
            "order_success.html",
            business=BUSINESS,
            reference=reference,
            lines=order_summary,
            total=order_total,
            paid_email=data.get("customer", {}).get("email", ""),
        )

    return render_template("order_failed.html", business=BUSINESS, reference=reference)


# ---------- Reservations ----------

@app.route("/reservations", methods=["POST"])
def reservations():
    """
    No booking database yet — this hands the request straight to the
    owner's WhatsApp with the details pre-filled, so it works today
    without needing a calendar/booking backend. Swap for a real booking
    system later if the owner wants automatic confirmations.
    """
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    date = request.form.get("date", "").strip()
    time = request.form.get("time", "").strip()
    guests = request.form.get("guests", "").strip()

    if not (name and phone and date and time and guests):
        flash("Please fill in every field to request a table.", "error")
        return redirect(url_for("home") + "#reservations")

    message = (
        f"Hi VMAX! I'd like to reserve a table.\n"
        f"Name: {name}\nPhone: {phone}\nDate: {date}\nTime: {time}\nGuests: {guests}"
    )
    import urllib.parse
    wa_url = f"https://wa.me/{BUSINESS['phone'].lstrip('+')}?text={urllib.parse.quote(message)}"
    return redirect(wa_url)


# ---------- Misc ----------

@app.route("/order")
def order_whatsapp():
    """Fallback: send visitors straight to WhatsApp instead of the cart."""
    return redirect(f"https://wa.me/{BUSINESS['phone'].lstrip('+')}")


@app.route("/api/menu")
def api_menu():
    return jsonify(MENU_ITEMS)


@app.route("/api/business-info")
def business_info():
    return jsonify(BUSINESS)


@app.route("/healthz")
def healthz():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(debug=True)
