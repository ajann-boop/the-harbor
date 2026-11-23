import os
import random
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "the-harbor-share-your-walk-secret-2026")

DATABASE_URL = os.environ.get("DATABASE_URL")
SMTP_EMAIL = os.environ.get("SMTP_EMAIL", "theharborshareyourwalk@gmail.com")
SMTP_APP_PASSWORD = os.environ.get("SMTP_APP_PASSWORD", "")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "theharborshareyourwalk@gmail.com")
ADMIN_PIN_PRIMARY = os.environ.get("ADMIN_PIN_PRIMARY", "4321")
ADMIN_PIN_SECONDARY = os.environ.get("ADMIN_PIN_SECONDARY", "1234")

UPLOAD_CONTEST_DIR = os.path.join("static", "uploads", "contest")
os.makedirs(UPLOAD_CONTEST_DIR, exist_ok=True)


def get_db_connection():
    if not DATABASE_URL:
        return None
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    conn = get_db_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS harbor_members (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(80),
                        first_name VARCHAR(80),
                        last_name VARCHAR(80),
                        caregiver_role VARCHAR(120),
                        email VARCHAR(160) UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        verification_code VARCHAR(10),
                        email_verified BOOLEAN DEFAULT FALSE,
                        is_approved BOOLEAN DEFAULT FALSE,
                        is_admin BOOLEAN DEFAULT FALSE,
                        bio TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cur.execute("""
                    ALTER TABLE harbor_members
                    ADD COLUMN IF NOT EXISTS is_moderator BOOLEAN DEFAULT FALSE;
                """)   
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS serious_wall_posts (
                        id SERIAL PRIMARY KEY,
                        category VARCHAR(80) NOT NULL,
                        topic VARCHAR(200) NOT NULL,
                        message TEXT NOT NULL,
                        author_name VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS serious_wall_replies (
                        id SERIAL PRIMARY KEY,
                        post_id INTEGER REFERENCES serious_wall_posts(id) ON DELETE CASCADE,
                        author_name VARCHAR(100) NOT NULL,
                        reply_text TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS harbor_contest_entries (
                        id SERIAL PRIMARY KEY,
                        week_key VARCHAR(20) NOT NULL,
                        round_code VARCHAR(20) NOT NULL,
                        caption VARCHAR(220) NOT NULL,
                        author_name VARCHAR(100) NOT NULL,
                        image_url TEXT NOT NULL,
                        votes INTEGER DEFAULT 0,
                        is_champion BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS harbor_contest_daily_votes (
                        id SERIAL PRIMARY KEY,
                        week_key VARCHAR(20) NOT NULL,
                        vote_date DATE NOT NULL DEFAULT CURRENT_DATE,
                        voter_key VARCHAR(160) NOT NULL,
                        entry_id INTEGER REFERENCES harbor_contest_entries(id) ON DELETE CASCADE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(week_key, vote_date, voter_key)
                    );
                """)
    except Exception as e:
        print("DB init warning:", e)
    finally:
        conn.close()


init_db()


def send_harbor_email(to_email, subject, html_body):
    if not SMTP_APP_PASSWORD:
        print(f"[DEV EMAIL] To: {to_email} | Subject: {subject}")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"The Harbor <{SMTP_EMAIL}>"
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_APP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print("SMTP email error:", e)
        return False


def get_mosaic_images():
    mosaic_dir = os.path.join(app.static_folder, "images", "mosaic")
    if not os.path.isdir(mosaic_dir):
        return []
    valid_exts = (".jpg", ".jpeg", ".png", ".webp", ".gif")
    return sorted([f for f in os.listdir(mosaic_dir) if f.lower().endswith(valid_exts)])


def get_contest_schedule_context(now=None):
    if now is None:
        now = datetime.datetime.now()
    iso_year, iso_week, _ = now.isocalendar()
    week_key = f"{iso_year}-W{iso_week:02d}"
    wd = now.weekday()  # Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6

    if wd == 5:
        phase_label = "Saturday Final Tally & Winner Reveal"
    elif wd == 6:
        phase_label = "Sunday Winner Acknowledgement"
    else:
        phase_label = "Daily Showdown Open — Cast 1 Vote Per Day"

    return {
        "week_key": week_key,
        "weekday": wd,
        "today_str": now.strftime("%Y-%m-%d"),
        "phase_label": phase_label,
    }


def tally_and_fetch_champion(conn, week_key, weekday):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM harbor_contest_entries
            WHERE week_key = %s AND is_champion = TRUE
            ORDER BY votes DESC, id ASC LIMIT 1;
        """, (week_key,))
        champ = cur.fetchone()

        if not champ and weekday in (5, 6):
            cur.execute("""
                SELECT * FROM harbor_contest_entries
                WHERE week_key = %s
                ORDER BY votes DESC, created_at ASC LIMIT 1;
            """, (week_key,))
            top_entry = cur.fetchone()
            if top_entry:
                cur.execute("""
                    UPDATE harbor_contest_entries
                    SET is_champion = TRUE
                    WHERE id = %s RETURNING *;
                """, (top_entry["id"],))
                champ = cur.fetchone()

        if not champ:
            cur.execute("""
                SELECT * FROM harbor_contest_entries
                WHERE is_champion = TRUE
                ORDER BY id DESC LIMIT 1;
            """)
            champ = cur.fetchone()

        return dict(champ) if champ else None


@app.route("/")
def index():
    mosaic_images = get_mosaic_images()
    weekly_champion = None
    conn = get_db_connection()
    if conn:
        try:
            sched = get_contest_schedule_context()
            weekly_champion = tally_and_fetch_champion(conn, sched["week_key"], sched["weekday"])
            conn.commit()
        except Exception as e:
            print("Index champion lookup warning:", e)
        finally:
            conn.close()
    return render_template("index.html", mosaic_images=mosaic_images, weekly_champion=weekly_champion)


# ---------------- REGISTRATION & LOGIN ---------------- #

@app.route("/api/register/send-code", methods=["POST"])
def register_send_code():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    caregiver_role = (data.get("caregiver_role") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not first_name or not last_name or not email or len(password) < 8:
        return jsonify({"ok": False, "error": "Please complete all required fields (password 8+ characters)."}), 400

    code = f"{random.randint(100000, 999999)}"
    pw_hash = generate_password_hash(password)

    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": False, "error": "Database connection unavailable."}), 500

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, is_approved FROM harbor_members WHERE email = %s;", (email,))
                existing = cur.fetchone()
                if existing and existing.get("is_approved"):
                    return jsonify({"ok": False, "error": "An approved account already exists for that email."}), 400

                if existing:
                    cur.execute("""
                        UPDATE harbor_members
                        SET username = %s, first_name = %s, last_name = %s,
                            caregiver_role = %s, password_hash = %s, verification_code = %s
                        WHERE email = %s;
                    """, (username, first_name, last_name, caregiver_role, pw_hash, code, email))
                else:
                    cur.execute("""
                        INSERT INTO harbor_members
                        (username, first_name, last_name, caregiver_role, email, password_hash, verification_code)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (username, first_name, last_name, caregiver_role, email, pw_hash, code))

        send_harbor_email(
            email,
            "The Harbor — Your 6-Digit Confirmation Code",
            f"<p>Hi {first_name},</p><p>Your confirmation code for <strong>The Harbor</strong> is:</p>"
            f"<h2 style='letter-spacing:4px; color:#0d9488;'>{code}</h2>"
            f"<p>Enter this code on the registration screen to complete your application.</p>"
        )
        return jsonify({"ok": True, "message": f"6-digit confirmation code sent to {email}!"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    finally:
        conn.close()


@app.route("/api/register/verify", methods=["POST"])
def register_verify():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    code = (data.get("code") or "").strip()
    bio = (data.get("bio") or "").strip()

    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": False, "error": "Database connection unavailable."}), 500

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM harbor_members WHERE email = %s;", (email,))
                member = cur.fetchone()
                if not member:
                    return jsonify({"ok": False, "error": "No pending registration found for that email."}), 404
                if (member.get("verification_code") or "") != code:
                    return jsonify({"ok": False, "error": "That 6-digit code does not match. Please double-check your email."}), 400

                cur.execute("""
                    UPDATE harbor_members
                    SET email_verified = TRUE, bio = %s, verification_code = NULL
                    WHERE email = %s;
                """, (bio, email))

        send_harbor_email(
            ADMIN_EMAIL,
            f"New Harbor Member Pending Review: {member.get('first_name')} {member.get('last_name')}",
            f"<p><strong>Name:</strong> {member.get('first_name')} {member.get('last_name')} (@{member.get('username')})</p>"
            f"<p><strong>Email:</strong> {email}</p>"
            f"<p><strong>Role:</strong> {member.get('caregiver_role')}</p>"
            f"<p><strong>About:</strong> {bio}</p>"
        )
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    finally:
        conn.close()


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    login_id = (data.get("login_id") or "").strip()
    password = (data.get("password") or "").strip()

    if not login_id or not password:
        return jsonify({"ok": False, "error": "Please enter both your login ID and password."}), 400

    owner_aliases = ("ajann", "admin", "anthony", "asianmama_1", ADMIN_EMAIL.lower())
    mod_aliases = ("mod", "moderator", "harbormod")

    # 1. Full Owner Fast-Path (Master PIN 4321)
    if login_id.lower() in owner_aliases and password == ADMIN_PIN_PRIMARY:
        session["member_id"] = 0
        session["display_name"] = "Anthony"
        session["is_admin"] = True
        session["admin_role"] = "owner"
        return jsonify({
            "ok": True,
            "display_name": "Anthony",
            "caregiver_role": "PC|🧸 Pediatric Caregiver",
            "bio": "Marcus, 15 and Rachel, 9",
            "is_admin": True,
            "admin_role": "owner"
        })

    # 2. Community Moderator Fast-Path (Moderator PIN 1234 — Verification & Community Q&A ONLY)
    if (login_id.lower() in mod_aliases or login_id.lower() in owner_aliases) and password == ADMIN_PIN_SECONDARY:
        session["member_id"] = 0
        session["display_name"] = "Community Moderator"
        session["is_admin"] = True
        session["admin_role"] = "moderator"
        return jsonify({
            "ok": True,
            "display_name": "Community Moderator",
            "caregiver_role": "🛡️ Community Moderator",
            "bio": "",
            "is_admin": True,
            "admin_role": "moderator"
        })

    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": False, "error": "Database connection unavailable."}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM harbor_members
                WHERE LOWER(email) = LOWER(%s) OR LOWER(username) = LOWER(%s)
                LIMIT 1;
            """, (login_id, login_id))
            member = cur.fetchone()

        if not member:
            return jsonify({"ok": False, "error": "Account not found."}), 401

        is_owner = bool(member.get("is_admin")) or (member.get("email", "").lower() == ADMIN_EMAIL.lower()) or (login_id.lower() in owner_aliases)
        is_mod = bool(member.get("is_moderator")) or (login_id.lower() in mod_aliases)

        valid_pw = (
            check_password_hash(member["password_hash"], password)
            or (is_owner and password == ADMIN_PIN_PRIMARY)
            or ((is_owner or is_mod) and password == ADMIN_PIN_SECONDARY)
        )
        if not valid_pw:
            return jsonify({"ok": False, "error": "Incorrect password."}), 401

        if not member.get("is_approved") and not (is_owner or is_mod):
            return jsonify({"ok": False, "error": "Your membership is still pending admin review (allow up to 24 hours)."}), 403

        admin_role = "owner" if (is_owner and password != ADMIN_PIN_SECONDARY) else ("moderator" if (is_owner or is_mod) else None)
        display_name = member.get("username") or member.get("first_name") or "Member"

        session["member_id"] = member["id"]
        session["display_name"] = display_name
        session["is_admin"] = bool(admin_role)
        session["admin_role"] = admin_role

        return jsonify({
            "ok": True,
            "display_name": display_name,
            "caregiver_role": member.get("caregiver_role") or "",
            "bio": member.get("bio") or "",
            "is_admin": bool(admin_role),
            "admin_role": admin_role
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    finally:
        conn.close()


@app.route("/api/change-password", methods=["POST"])
def api_change_password():
    member_id = session.get("member_id")
    if not member_id:
        return jsonify({"ok": False, "error": "Please log in first to update your password."}), 401

    data = request.get_json(silent=True) or {}
    cur_pw = data.get("current_password") or ""
    new_pw = data.get("new_password") or ""
    if len(new_pw) < 6:
        return jsonify({"ok": False, "error": "New password must be at least 6 characters."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": False, "error": "Database unavailable."}), 500

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT password_hash FROM harbor_members WHERE id = %s;", (member_id,))
                row = cur.fetchone()
                if not row or not check_password_hash(row["password_hash"], cur_pw):
                    return jsonify({"ok": False, "error": "Current password is incorrect."}), 400
                cur.execute(
                    "UPDATE harbor_members SET password_hash = %s WHERE id = %s;",
                    (generate_password_hash(new_pw), member_id)
                )
        return jsonify({"ok": True, "message": "Password updated successfully!"})
    finally:
        conn.close()


# ---------------- ADMIN REVIEW ENDPOINTS ---------------- #

@app.route("/api/admin/members", methods=["GET"])
def api_admin_members():
    if not session.get("is_admin"):
        return jsonify({"ok": False, "error": "Admin access required."}), 403
    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": True, "members": []})
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, first_name, last_name, caregiver_role, email, bio, created_at
                FROM harbor_members
                WHERE is_approved = FALSE
                ORDER BY created_at DESC;
            """)
            members = [dict(r) for r in cur.fetchall()]
        return jsonify({"ok": True, "members": members})
    finally:
        conn.close()


@app.route("/api/admin/members/<int:member_id>/<action>", methods=["POST"])
def api_admin_review_member(member_id, action):
    if not session.get("is_admin"):
        return jsonify({"ok": False, "error": "Admin access required."}), 403
    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": False, "error": "Database unavailable."}), 500
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM harbor_members WHERE id = %s;", (member_id,))
                member = cur.fetchone()
                if not member:
                    return jsonify({"ok": False, "error": "Member not found."}), 404

                if action == "approve":
                    cur.execute("UPDATE harbor_members SET is_approved = TRUE WHERE id = %s;", (member_id,))
                    send_harbor_email(
                        member["email"],
                        "Welcome to The Harbor — Your Membership is Approved!",
                        f"<p>Hi {member.get('first_name')},</p>"
                        f"<p>Welcome to <strong>The Harbor</strong>! Your membership has been approved. "
                        f"You can now log in anytime at <a href='https://shareyourwalk.com'>shareyourwalk.com</a>.</p>"
                    )
                elif action == "decline":
                    cur.execute("DELETE FROM harbor_members WHERE id = %s;", (member_id,))
                else:
                    return jsonify({"ok": False, "error": "Invalid action."}), 400
        return jsonify({"ok": True})
    finally:
        conn.close()


# ---------------- WALL OF SERIOUSNESS ENDPOINTS ---------------- #

@app.route("/api/wall", methods=["GET", "POST"])
def api_serious_wall():
    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": True, "posts": []})

    if request.method == "GET":
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM serious_wall_posts ORDER BY created_at DESC;")
                posts = [dict(r) for r in cur.fetchall()]
                for p in posts:
                    cur.execute(
                        "SELECT * FROM serious_wall_replies WHERE post_id = %s ORDER BY created_at ASC;",
                        (p["id"],)
                    )
                    p["replies"] = [dict(rep) for rep in cur.fetchall()]
            return jsonify({"ok": True, "posts": posts})
        finally:
            conn.close()

    data = request.get_json(silent=True) or {}
    category = (data.get("category") or "⏳ Time-Sensitive").strip()
    topic = (data.get("topic") or "").strip()
    message = (data.get("message") or "").strip()
    author_name = (data.get("author_name") or session.get("display_name") or "A Fellow Caregiver").strip()

    if not topic or not message:
        conn.close()
        return jsonify({"ok": False, "error": "Headline and question are required."}), 400

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO serious_wall_posts (category, topic, message, author_name)
                    VALUES (%s, %s, %s, %s) RETURNING id;
                """, (category, topic, message, author_name))
                new_id = cur.fetchone()["id"]
        return jsonify({"ok": True, "id": new_id})
    finally:
        conn.close()


@app.route("/api/wall/<int:post_id>/reply", methods=["POST"])
def api_serious_wall_reply(post_id):
    data = request.get_json(silent=True) or {}
    reply_text = (data.get("reply_text") or "").strip()
    author_name = (data.get("author_name") or session.get("display_name") or "A Fellow Caregiver").strip()
    if not reply_text:
        return jsonify({"ok": False, "error": "Reply cannot be empty."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": False, "error": "Database unavailable."}), 500
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO serious_wall_replies (post_id, author_name, reply_text)
                    VALUES (%s, %s, %s);
                """, (post_id, author_name, reply_text))
        return jsonify({"ok": True})
    finally:
        conn.close()


@app.route("/api/wall/<int:post_id>", methods=["DELETE"])
def api_serious_wall_delete(post_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": False, "error": "Database unavailable."}), 500
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM serious_wall_posts WHERE id = %s;", (post_id,))
        return jsonify({"ok": True})
    finally:
        conn.close()


# ---------------- CONTEST (SIDE-BY-SIDE TUES/THURS SHOWDOWN -> 1 VOTE/DAY -> SAT TALLY -> SUN SPOTLIGHT) ---------------- #

@app.route("/api/contest/state", methods=["GET"])
def api_contest_state():
    sched = get_contest_schedule_context()
    voter_key = (request.args.get("voter_name") or session.get("display_name") or request.remote_addr or "guest").strip()
    conn = get_db_connection()
    if not conn:
        return jsonify({
            "ok": True,
            "schedule": sched,
            "tuesday_pick": None,
            "thursday_pick": None,
            "round_entries": [],
            "voted_today": False,
            "weekly_champion": None
        })

    try:
        weekly_champion = tally_and_fetch_champion(conn, sched["week_key"], sched["weekday"])
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM harbor_contest_entries
                WHERE week_key = %s
                ORDER BY votes DESC, created_at DESC;
            """, (sched["week_key"],))
            round_entries = [dict(r) for r in cur.fetchall()]

            cur.execute("""
                SELECT * FROM harbor_contest_entries
                WHERE week_key = %s AND round_code = 'TUE'
                ORDER BY votes DESC, created_at ASC LIMIT 1;
            """, (sched["week_key"],))
            tue_row = cur.fetchone()

            cur.execute("""
                SELECT * FROM harbor_contest_entries
                WHERE week_key = %s AND round_code = 'THU'
                ORDER BY votes DESC, created_at ASC LIMIT 1;
            """, (sched["week_key"],))
            thu_row = cur.fetchone()

            # Fallback if only 2 entries exist without separate round codes
            if not tue_row and len(round_entries) >= 1:
                tue_row = round_entries[0]
            if not thu_row and len(round_entries) >= 2:
                thu_row = round_entries[1]

            cur.execute("""
                SELECT id FROM harbor_contest_daily_votes
                WHERE week_key = %s AND vote_date = CURRENT_DATE AND voter_key = %s
                LIMIT 1;
            """, (sched["week_key"], voter_key))
            voted_today = bool(cur.fetchone())

        conn.commit()
        return jsonify({
            "ok": True,
            "schedule": sched,
            "tuesday_pick": dict(tue_row) if tue_row else None,
            "thursday_pick": dict(thu_row) if thu_row else None,
            "round_entries": round_entries,
            "voted_today": voted_today,
            "weekly_champion": weekly_champion
        })
    finally:
        conn.close()


@app.route("/api/contest/upload", methods=["POST"])
def api_contest_upload():
    photo = request.files.get("photo")
    caption = (request.form.get("caption") or "Caregiver Snapshot").strip()
    author_name = (request.form.get("author_name") or session.get("display_name") or "Member").strip()

    if not photo or not photo.filename:
        return jsonify({"ok": False, "error": "Please select a photo to upload."}), 400

    sched = get_contest_schedule_context()
    round_code = "TUE" if sched["weekday"] in (6, 0, 1) else "THU"

    safe_name = secure_filename(f"{sched['week_key']}_{round_code}_{random.randint(1000,9999)}_{photo.filename}")
    save_path = os.path.join(UPLOAD_CONTEST_DIR, safe_name)
    photo.save(save_path)
    image_url = f"/static/uploads/contest/{safe_name}"

    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": False, "error": "Database unavailable."}), 500

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO harbor_contest_entries (week_key, round_code, caption, author_name, image_url)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (sched["week_key"], round_code, caption, author_name, image_url))
                entry_id = cur.fetchone()["id"]
        return jsonify({"ok": True, "id": entry_id, "round_code": round_code})
    finally:
        conn.close()


@app.route("/api/contest/vote", methods=["POST"])
def api_contest_vote():
    data = request.get_json(silent=True) or {}
    entry_id = data.get("entry_id")
    voter_name = (data.get("voter_name") or session.get("display_name") or request.remote_addr or "guest").strip()

    if not entry_id:
        return jsonify({"ok": False, "error": "Missing entry ID."}), 400

    sched = get_contest_schedule_context()
    conn = get_db_connection()
    if not conn:
        return jsonify({"ok": False, "error": "Database unavailable."}), 500

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO harbor_contest_daily_votes (week_key, vote_date, voter_key, entry_id)
                    VALUES (%s, CURRENT_DATE, %s, %s)
                    ON CONFLICT (week_key, vote_date, voter_key) DO NOTHING
                    RETURNING id;
                """, (sched["week_key"], voter_name, entry_id))
                inserted = cur.fetchone()
                if not inserted:
                    return jsonify({
                        "ok": False,
                        "error": "You already cast today's vote! Come back tomorrow to vote again before Saturday's final tally."
                    }), 400
                cur.execute("UPDATE harbor_contest_entries SET votes = votes + 1 WHERE id = %s;", (entry_id,))
        return jsonify({"ok": True})
    finally:
        conn.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)