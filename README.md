# VMAX Tea & Coffee Shop — Website

# VMAX Tea & Coffee Shop — Website

Flask site for VMAX Tea And Coffee Shop, Uyo — with a real shopping cart
and Paystack checkout.

## Project structure

```
vmax-tea-coffee/
├── app.py                 # Flask app, routes, business info
├── menu.py                 # Menu items (single source of truth for prices)
├── cart.py                 # Session-based cart logic
├── paystack.py              # Paystack API wrapper (initialize/verify)
├── requirements.txt
├── .env.example             # Copy to .env and fill in real keys
├── templates/
│   ├── _header.html / _footer.html   # Shared nav/footer
│   ├── index.html            # Home page + menu with add-to-cart
│   ├── cart.html             # Cart page
│   ├── checkout.html          # Checkout form
│   ├── order_success.html      # Shown after a successful payment
│   └── order_failed.html       # Shown if payment fails/cancels
├── static/
│   ├── css/style.css          # Main site styles
│   ├── css/shop.css           # Cart/checkout/order page styles
│   └── js/script.js           # Menu tabs, scroll reveal, mobile nav
└── README.md
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
cp .env.example .env
```

Then open `.env` and fill in:
- `PAYSTACK_SECRET_KEY` / `PAYSTACK_PUBLIC_KEY` — get test keys free, instantly,
  at https://dashboard.paystack.com/#/settings/developer (no approval wait —
  test keys work immediately with fake card numbers)
- `FLASK_SECRET_KEY` — any random long string, used to sign the cart's session cookie

```bash
python app.py
```

Visit `http://127.0.0.1:5000`.

## How the checkout flow works

1. Customer adds items on the home page → stored in their session (cart.py)
2. `/cart` — review, change quantity, remove items
3. `/checkout` — enters name/email/phone → app calls Paystack's
   `transaction/initialize` endpoint → customer is redirected to Paystack's
   hosted payment page (their card details never touch this app)
4. After paying, Paystack redirects back to `/checkout/callback` — the app
   calls Paystack's `transaction/verify` endpoint to **confirm server-side**
   that the payment actually succeeded (never trust the redirect alone)
5. On success: cart is cleared, receipt page shown, Paystack emails a receipt too

## Testing payments

With **test** keys, Paystack lets you "pay" with fake card numbers —
see https://paystack.com/docs/payments/test-payments for current test
card numbers. No real money moves.

## Going live

1. Owner completes KYC on Paystack (business details, bank account for payouts)
2. Swap `.env` from test keys (`sk_test_...`) to live keys (`sk_live_...`)
3. Deploy (see below) — that's it, real payments start working

## Routes

| Route                  | What it does                                     |
|-------------------------|---------------------------------------------------|
| `/`                      | The site + shoppable menu                        |
| `/cart`                  | View/edit cart                                    |
| `/checkout`               | Enter details, start Paystack payment             |
| `/checkout/callback`         | Paystack redirects here after payment              |
| `/order`                  | Redirects to WhatsApp (fallback ordering option)   |
| `/api/menu`                | JSON menu data                                    |
| `/api/business-info`          | JSON — address, phone, hours, rating              |
| `/healthz`                 | Health check                                       |

## Editing business info or menu

- Address/phone/hours/rating: `BUSINESS` dict at the top of `app.py`
- Menu items and prices: `menu.py` — update `price` there and it flows
  through cart, checkout, and receipts automatically

## Content still needed from the owner

Sections marked `<!-- PLACEHOLDER -->` in `templates/index.html` use
realistic sample copy and need real content: brand story, final menu
and prices, loyalty program details, testimonials, logo, and photos.

## Deploying

This app now needs a persistent Python server (session-based cart,
server-to-server Paystack calls) — **Render**, not Vercel's static/serverless
hosting. Push to GitHub, connect the repo on Render, set:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Environment variables: add `PAYSTACK_SECRET_KEY`, `PAYSTACK_PUBLIC_KEY`,
  `FLASK_SECRET_KEY` in Render's dashboard (never commit `.env` to GitHub)

