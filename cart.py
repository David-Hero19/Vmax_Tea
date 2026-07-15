"""
Session-based shopping cart. No database needed — the cart lives in the
customer's browser session (a signed cookie), so it's simple and works
fine for a small shop's order volume. It resets if they clear cookies
or switch devices, which is an acceptable tradeoff for this use case.
"""

from flask import session
from menu import get_item

CART_KEY = "cart"


def _cart():
    if CART_KEY not in session:
        session[CART_KEY] = {}
    return session[CART_KEY]


def add(item_id, quantity=1):
    item = get_item(item_id)
    if not item:
        return False
    cart = _cart()
    cart[item_id] = cart.get(item_id, 0) + quantity
    session[CART_KEY] = cart
    session.modified = True
    return True


def remove(item_id):
    cart = _cart()
    cart.pop(item_id, None)
    session[CART_KEY] = cart
    session.modified = True


def set_quantity(item_id, quantity):
    cart = _cart()
    if quantity <= 0:
        cart.pop(item_id, None)
    else:
        cart[item_id] = quantity
    session[CART_KEY] = cart
    session.modified = True


def clear():
    session[CART_KEY] = {}
    session.modified = True


def contents():
    """Returns a list of {item, quantity, line_total} for display."""
    cart = _cart()
    lines = []
    for item_id, qty in cart.items():
        item = get_item(item_id)
        if item:
            lines.append({
                "item": item,
                "quantity": qty,
                "line_total": item["price"] * qty,
            })
    return lines


def total():
    return sum(line["line_total"] for line in contents())


def item_count():
    return sum(_cart().values())
