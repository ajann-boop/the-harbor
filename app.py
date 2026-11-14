import psycopg2
from psycopg2.extras import RealDictCursor
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


def get_mosaic_images():
    folder = os.path.join(app.static_folder or 'static', 'images', 'mosaic')
    if not os.path.isdir(folder):
        return []
    exts = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(exts)])
    return [f"/static/images/mosaic/{f}" for f in files]

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



@app.route("/api/founder-recovery", methods=["POST"])
def founder_recovery():
    if not supabase:
        return jsonify({"error": "Auth service not configured"}), 500
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    pin = str(data.get("pin") or "").strip()
    expected_pin = os.environ.get("ADMIN_PIN", "")
    founder_email = os.environ.get("ADMIN_NOTIFY_EMAIL", "a.s.jannuzzi@gmail.com").strip().lower()
    if not expected_pin or pin != expected_pin:
        return jsonify({"error": "Invalid Founder Recovery Key"}), 403
    if email != founder_email:
        return jsonify({"error": "Email does not match founder account"}), 403
    try:
        supabase.auth.reset_password_for_email(
            email,
            {"redirect_to": "https://www.shareyourwalk.com/"}
        )
        return jsonify({"ok": True, "message": f"Password reset email sent to {email}!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400



@app.route("/api/update-password", methods=["POST"])
def update_password():
    if not supabase:
        return jsonify({"error": "Auth service not configured"}), 500
    data = request.get_json(silent=True) or {}
    access_token = (data.get("access_token") or "").strip()
    refresh_token = (data.get("refresh_token") or "").strip()
    new_password = data.get("new_password") or ""
    if not access_token or len(new_password) < 8:
        return jsonify({"error": "Valid recovery session and password (8+ chars) required"}), 400
    try:
        supabase.auth.set_session(access_token, refresh_token or access_token)
        res = supabase.auth.update_user({"password": new_password})
        return jsonify({"ok": True, "message": "Password updated! You can now sign in."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400



DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_conn():
    return psycopg2.connect(DATABASE_URL) if DATABASE_URL else None

def init_chat_tables():
    conn = get_db_conn()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id SERIAL PRIMARY KEY,
                    room_name TEXT NOT NULL,
                    sender_handle TEXT NOT NULL,
                    sender_email TEXT,
                    message_text TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_presence (
                    session_token TEXT PRIMARY KEY,
                    room_name TEXT NOT NULL,
                    member_handle TEXT NOT NULL,
                    last_seen TIMESTAMPTZ DEFAULT NOW()
                );
            """)
        conn.commit()
    except Exception as e:
        print("Chat DB init error:", e)
    finally:
        conn.close()

init_chat_tables()

@app.route("/api/chat/state", methods=["GET", "POST"])
def chat_state():
    data = request.get_json(silent=True) or {}
    room = (request.args.get("room") or data.get("room") or "Village Chat Room").strip()
    client_id = (request.args.get("client_id") or data.get("client_id") or "").strip()
    user = session.get("user") or {}
    handle = (data.get("handle") or user.get("handle") or (user.get("email", "").split("@")[0] if user.get("email") else "CaregiverGuest")).strip()
    conn = get_db_conn()
    if not conn:
        return jsonify({"messages": [], "room_active": 1, "total_active": 1})
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if client_id:
                cur.execute("""
                    INSERT INTO chat_presence (session_token, room_name, member_handle, last_seen)
                    VALUES (%s, %s, %s, NOW())
                    ON CONFLICT (session_token)
                    DO UPDATE SET room_name = EXCLUDED.room_name, member_handle = EXCLUDED.member_handle, last_seen = NOW();
                """, (client_id, room, handle))
            cur.execute("DELETE FROM chat_presence WHERE last_seen < NOW() - INTERVAL '20 seconds';")
            cur.execute("SELECT COUNT(DISTINCT session_token) AS cnt FROM chat_presence WHERE room_name = %s;", (room,))
            room_active = max(1, int(cur.fetchone()["cnt"] or 1))
            cur.execute("SELECT COUNT(DISTINCT session_token) AS cnt FROM chat_presence;")
            total_active = max(1, int(cur.fetchone()["cnt"] or 1))
            cur.execute("""
                SELECT id, room_name, sender_handle, message_text,
                       TO_CHAR(created_at AT TIME ZONE 'America/New_York', 'HH12:MI AM') AS time_str
                FROM chat_messages WHERE room_name = %s ORDER BY id DESC LIMIT 60;
            """, (room,))
            rows = list(reversed(cur.fetchall()))
        conn.commit()
        return jsonify({"messages": rows, "room_active": room_active, "total_active": total_active})
    except Exception as e:
        return jsonify({"error": str(e), "messages": [], "room_active": 1, "total_active": 1}), 500
    finally:
        conn.close()

@app.route("/api/chat/send", methods=["POST"])
def chat_send():
    data = request.get_json(silent=True) or {}
    room = (data.get("room") or "Village Chat Room").strip()
    text = (data.get("message") or "").strip()[:1000]
    if not text:
        return jsonify({"error": "Message cannot be empty"}), 400
    user = session.get("user") or {}
    sender_email = user.get("email", "")
    sender_handle = (data.get("handle") or user.get("handle") or (sender_email.split("@")[0] if sender_email else "CaregiverMember")).strip()
    conn = get_db_conn()
    if not conn:
        return jsonify({"error": "Database not connected"}), 500
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO chat_messages (room_name, sender_handle, sender_email, message_text)
                VALUES (%s, %s, %s, %s)
                RETURNING id, room_name, sender_handle, message_text,
                          TO_CHAR(created_at AT TIME ZONE 'America/New_York', 'HH12:MI AM') AS time_str;
            """, (room, sender_handle, sender_email, text))
            msg = cur.fetchone()
        conn.commit()
        return jsonify({"ok": True, "message": msg})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/chat/leave", methods=["POST"])
def chat_leave():
    data = request.get_json(silent=True) or {}
    client_id = (data.get("client_id") or "").strip()
    conn = get_db_conn()
    if conn and client_id:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM chat_presence WHERE session_token = %s;", (client_id,))
            conn.commit()
        finally:
            conn.close()
    return jsonify({"ok": True})



# --- COMMUNITY CORK BOARD (ADVICE & ZERO-PROFIT GIFT/LOAN BOARD) ---
def init_corkboard_tables():
    conn = get_db_conn()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS corkboard_notes (
                    id SERIAL PRIMARY KEY,
                    note_type TEXT NOT NULL DEFAULT 'advice',
                    author_handle TEXT NOT NULL,
                    author_email TEXT,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    zip_code TEXT DEFAULT '',
                    photo_data TEXT DEFAULT '',
                    pin_color TEXT DEFAULT '#ef4444',
                    note_color TEXT DEFAULT '#fef08a',
                    tilt_deg NUMERIC(4,1) DEFAULT 0.0,
                    is_claimed BOOLEAN DEFAULT FALSE,
                    is_flagged BOOLEAN DEFAULT FALSE,
                    flag_reason TEXT DEFAULT '',
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS corkboard_replies (
                    id SERIAL PRIMARY KEY,
                    note_id INTEGER REFERENCES corkboard_notes(id) ON DELETE CASCADE,
                    author_handle TEXT NOT NULL,
                    reply_text TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
        conn.commit()
    except Exception as e:
        print("Corkboard DB init error:", e)
    finally:
        conn.close()

init_corkboard_tables()

@app.route("/api/corkboard", methods=["GET"])
def get_corkboard():
    filter_type = (request.args.get("type") or "all").strip().lower()
    zip_q = (request.args.get("zip") or "").strip()
    conn = get_db_conn()
    if not conn:
        return jsonify({"notes": []})
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
                SELECT id, note_type, author_handle, title, body, zip_code, photo_data,
                       pin_color, note_color, tilt_deg, is_claimed, is_flagged, flag_reason,
                       TO_CHAR(created_at AT TIME ZONE 'America/New_York', 'Mon DD, HH12:MI AM') AS time_str
                FROM corkboard_notes
                WHERE 1=1
            """
            params = []
            if filter_type in ("advice", "item"):
                query += " AND note_type = %s"
                params.append(filter_type)
            if zip_q:
                query += " AND zip_code ILIKE %s"
                params.append(f"%{zip_q}%")
            query += " ORDER BY is_claimed ASC, id DESC LIMIT 60;"
            cur.execute(query, params)
            notes = cur.fetchall()

            note_ids = [n["id"] for n in notes]
            replies_map = {nid: [] for nid in note_ids}
            if note_ids:
                cur.execute("""
                    SELECT id, note_id, author_handle, reply_text,
                           TO_CHAR(created_at AT TIME ZONE 'America/New_York', 'Mon DD, HH12:MI AM') AS time_str
                    FROM corkboard_replies
                    WHERE note_id = ANY(%s)
                    ORDER BY id ASC;
                """, (note_ids,))
                for r in cur.fetchall():
                    replies_map[r["note_id"]].append(r)

            for n in notes:
                n["tilt_deg"] = float(n["tilt_deg"] or 0.0)
                n["replies"] = replies_map.get(n["id"], [])
        return jsonify({"notes": notes})
    except Exception as e:
        return jsonify({"error": str(e), "notes": []}), 500
    finally:
        conn.close()

@app.route("/api/corkboard/pin", methods=["POST"])
def pin_corkboard_note():
    import random
    data = request.get_json(silent=True) or {}
    note_type = (data.get("note_type") or "advice").strip().lower()
    title = (data.get("title") or "").strip()[:120]
    body = (data.get("body") or "").strip()[:1200]
    zip_code = (data.get("zip_code") or "").strip()[:25]
    photo_data = (data.get("photo_data") or "").strip()
    free_pledge = bool(data.get("free_pledge"))

    if not title or not body:
        return jsonify({"error": "Please include a headline and note message."}), 400
    if note_type == "item" and not free_pledge:
        return jsonify({"error": "You must check the 100% Free Gift/Loan Pledge before pinning an item."}), 400
    if len(photo_data) > 650000:
        return jsonify({"error": "Photo is too large. Please pick a smaller image."}), 400

    user = session.get("user") or {}
    email = user.get("email", "")
    handle = (data.get("handle") or user.get("handle") or (email.split("@")[0] if email else "CaregiverMember")).strip()

    pin_colors = ["#ef4444", "#3b82f6", "#22c55e", "#f59e0b", "#ec4899", "#a855f7", "#06b6d4"]
    note_colors = ["#fef08a", "#bae6fd", "#fecdd3", "#bbf7d0", "#fed7aa", "#e9d5ff"]
    pin_color = random.choice(pin_colors)
    note_color = random.choice(note_colors)
    tilt_deg = round(random.uniform(-2.2, 2.2), 1)

    conn = get_db_conn()
    if not conn:
        return jsonify({"error": "Database not connected"}), 500
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO corkboard_notes
                (note_type, author_handle, author_email, title, body, zip_code, photo_data, pin_color, note_color, tilt_deg)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (note_type, handle, email, title, body, zip_code, photo_data, pin_color, note_color, tilt_deg))
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/corkboard/reply", methods=["POST"])
def reply_corkboard_note():
    data = request.get_json(silent=True) or {}
    note_id = data.get("note_id")
    reply_text = (data.get("reply_text") or "").strip()[:600]
    if not note_id or not reply_text:
        return jsonify({"error": "Reply cannot be empty"}), 400
    user = session.get("user") or {}
    email = user.get("email", "")
    handle = (data.get("handle") or user.get("handle") or (email.split("@")[0] if email else "CaregiverMember")).strip()
    conn = get_db_conn()
    if not conn:
        return jsonify({"error": "Database not connected"}), 500
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO corkboard_replies (note_id, author_handle, reply_text) VALUES (%s, %s, %s);", (note_id, handle, reply_text))
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/corkboard/flag", methods=["POST"])
def flag_corkboard_note():
    data = request.get_json(silent=True) or {}
    note_id = data.get("note_id")
    reason = (data.get("reason") or "Suspected selling / marketplace violation").strip()[:250]
    conn = get_db_conn()
    if not conn or not note_id:
        return jsonify({"error": "Invalid request"}), 400
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE corkboard_notes SET is_flagged = TRUE, flag_reason = %s WHERE id = %s;", (reason, note_id))
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/corkboard/claim", methods=["POST"])
def claim_corkboard_note():
    data = request.get_json(silent=True) or {}
    note_id = data.get("note_id")
    conn = get_db_conn()
    if not conn or not note_id:
        return jsonify({"error": "Invalid request"}), 400
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE corkboard_notes SET is_claimed = NOT is_claimed WHERE id = %s;", (note_id,))
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/corkboard/admin-delete", methods=["POST"])
def admin_delete_corkboard_note():
    data = request.get_json(silent=True) or {}
    pin = (data.get("pin") or "").strip()
    note_id = data.get("note_id")
    if pin != os.environ.get("ADMIN_PIN", "4321"):
        return jsonify({"error": "Invalid Admin PIN"}), 403
    conn = get_db_conn()
    if not conn or not note_id:
        return jsonify({"error": "Invalid request"}), 400
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM corkboard_notes WHERE id = %s;", (note_id,))
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)
