import os
from functools import wraps
from flask import Flask, render_template, request, jsonify, session
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-local-fallback-key")

is_prod = os.environ.get("RENDER") is not None
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=is_prod,
    SESSION_COOKIE_SAMESITE="Lax",
)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated


@app.route("/google155e5a17fdae6bf2.html")
def google_verification():
    return render_template("google155e5a17fdae6bf2.html")


@app.route("/")
def home():
    return render_template("index.html", mosaic_images=get_mosaic_images())


@app.route("/api/me", methods=["GET"])
def current_user():
    return jsonify({"user": session.get("user")})


@app.route("/api/signup", methods=["POST"])
def signup():
    if not supabase:
        return jsonify({"error": "Auth service not configured"}), 500
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("assword") or data.get("password") or ""
    display_name = (data.get("display_name") or "").strip()

    if not email or len(password) < 8:
        return jsonify({"error": "Valid email and password (8+ characters) required"}), 400

    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"display_name": display_name or email.split("@")[0]},
                "email_redirect_to": "https://www.shareyourwalk.com/"
            }
        })
        if res.user:
            session["user"] = {
                "id": res.user.id,
                "email": res.user.email,
                "display_name": display_name or email.split("@")[0],
            }
            return jsonify({

                "message": "Account created! Check your email if confirmation is enabled.",
                "user": session["user"],
                "needs_confirmation": res.session is None
            })
        return jsonify({"error": "Could not create account"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/login", methods=["POST"])
def login():
    if not supabase:
        return jsonify({"error": "Auth service not configured"}), 500
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            meta = res.user.user_metadata or {}
            session["user"] = {
                "id": res.user.id,
                "email": res.user.email,
                "display_name": meta.get("display_name") or email.split("@")[0],
            }
            return jsonify({"message": "Signed in", "user": session["user"]})
        return jsonify({error: "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": "Invalid email or password"}), 401


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({message: "Signed out"})


@app.route("/api/admin/verify", methods=["POST"])
def verify_admin():
    data = request.get_json(silent=True) or {}
    pin = str(data.get("pin") or "")
    expected_pin = os.environ.get("ADMIN_PIN", "")
    if expected_pin and pin == expected_pin:
        session["is_admin"] = True
        return jsonify({"verified": True})
    return jsonify({"verified": False, "error": "Invalid Admin PIN"}), 403



@app.route('/api/guest-inquiry', methods=['POST'])
def api_guest_inquiry():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    support_type = (data.get("support_type") or "Donor / Visitor Inquiry").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"error": "Please enter your name, email, and a short message."}), 400

    record = {
        "name": name,
        "email": email,
        "phone": phone,
        "support_type": support_type,
        "message": message
    }

    # 1. Save to Supabase table 'donor_inquiries' if configured
    saved_db = False
    if supabase:
        try:
            supabase.table("donor_inquiries").insert(record).execute()
            saved_db = True
        except Exception as e:
            print("Supabase donor_inquiries insert note:", e)

    # 2. Also append to local fallback JSONL so no inquiry is ever lost
    try:
        import json, datetime
        record["submitted_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        with open("guest_inquiries.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        print("Local inquiry log note:", e)

    # 3. Optional SMTP notification straight to Anthony if SMTP env vars exist
    try:
        import smtplib
        from email.message import EmailMessage
        smtp_user = os.environ.get("SMTP_USER")
        smtp_pass = os.environ.get("SMTP_PASS")
        notify_to = os.environ.get("ADMIN_NOTIFY_EMAIL", "a.s.jannuzzi@gmail.com")
        if smtp_user and smtp_pass:
            msg = EmailMessage()
            msg["Subject"] = f"[Share Your Walk] New {support_type} from {name}"
            msg["From"] = smtp_user
            msg["To"] = notify_to
            msg.set_content(
                f"New Donor / Visitor Inquiry (Bypassed Verification)\n\n"
                f"Name / Organization: {name}\n"
                f"Email: {email}\n"
                f"Phone / Contact: {phone or 'Not provided'}\n"
                f"Category: {support_type}\n\n"
                f"Message:\n{message}\n"
            )
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
    except Exception as e:
        print("SMTP notify note:", e)

    return jsonify({
        "ok": True,
        "saved_db": saved_db,
        "message": "Thank you! Your message has been sent directly to Anthony at Share Your Walk. We will reach out to you personally soon."
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
