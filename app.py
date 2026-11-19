import os
import random
import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from zoneinfo import ZoneInfo

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or secrets.token_hex(32)

DATABASE_URL = os.getenv("DATABASE_URL")
MASTER_PIN = os.getenv("MASTER_PIN", "")
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_APP_PASSWORD = os.getenv("MAIL_APP_PASSWORD", "")
HARBOR_CONTACT_EMAIL = os.getenv("HARBOR_CONTACT_EMAIL") or MAIL_USERNAME


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured.")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    """Create core tables in Supabase PostgreSQL if they do not exist yet."""
    if not DATABASE_URL:
        return
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS harbor_members (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(120) DEFAULT '',
                    display_name VARCHAR(120) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash TEXT DEFAULT '',
                    caregiver_role VARCHAR(160) DEFAULT '',
                    bio TEXT DEFAULT '',
                    is_verified BOOLEAN DEFAULT FALSE,
                    is_approved BOOLEAN DEFAULT FALSE,
                    verification_code VARCHAR(10),
                    code_expires_at TIMESTAMPTZ,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute("ALTER TABLE harbor_members ADD COLUMN IF NOT EXISTS username VARCHAR(120) DEFAULT '';")
            cur.execute("ALTER TABLE harbor_members ADD COLUMN IF NOT EXISTS bio TEXT DEFAULT '';")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS harbor_inquiries (
                    id SERIAL PRIMARY KEY,
                    sender_name VARCHAR(120) NOT NULL,
                    sender_email VARCHAR(255) NOT NULL,
                    sender_phone VARCHAR(60) DEFAULT '',
                    contact_pref VARCHAR(80) DEFAULT 'Email only',
                    inquiry_type VARCHAR(120) DEFAULT 'Guests & Contributors',
                    cause_designation VARCHAR(200) DEFAULT '',
                    message TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute("ALTER TABLE harbor_inquiries ADD COLUMN IF NOT EXISTS sender_phone VARCHAR(60) DEFAULT '';")
            cur.execute("ALTER TABLE harbor_inquiries ADD COLUMN IF NOT EXISTS contact_pref VARCHAR(80) DEFAULT 'Email only';")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS harbor_pic_entries (
                    id SERIAL PRIMARY KEY,
                    week_key VARCHAR(20) NOT NULL,
                    round_code VARCHAR(20) NOT NULL,
                    author_name VARCHAR(120) NOT NULL,
                    caption TEXT NOT NULL,
                    image_url TEXT NOT NULL,
                    votes INTEGER DEFAULT 0,
                    is_round_winner BOOLEAN DEFAULT FALSE,
                    is_weekly_champion BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS harbor_pic_votes (
                    id SERIAL PRIMARY KEY,
                    week_key VARCHAR(20) NOT NULL,
                    round_code VARCHAR(20) NOT NULL,
                    voter_key VARCHAR(160) NOT NULL,
                    entry_id INTEGER NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    UNIQUE (week_key, round_code, voter_key)
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS harbor_wall_posts (
                    id SERIAL PRIMARY KEY,
                    category VARCHAR(80) NOT NULL,
                    topic VARCHAR(200) NOT NULL,
                    message TEXT NOT NULL,
                    author_name VARCHAR(120) NOT NULL,
                    hugs INTEGER DEFAULT 0,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS harbor_wall_replies (
                    id SERIAL PRIMARY KEY,
                    post_id INTEGER NOT NULL REFERENCES harbor_wall_posts(id) ON DELETE CASCADE,
                    author_name VARCHAR(120) NOT NULL,
                    reply_text TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
        conn.commit()
    finally:
        conn.close()


def send_harbor_email(to_address, subject, body_text):
    """Send an email via Gmail SMTP using MAIL_USERNAME and MAIL_APP_PASSWORD."""
    if not MAIL_USERNAME or not MAIL_APP_PASSWORD:
        raise RuntimeError("MAIL_USERNAME or MAIL_APP_PASSWORD is missing.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"The Harbor <{MAIL_USERNAME}>"
    msg["To"] = to_address
    msg.set_content(body_text)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(MAIL_USERNAME, MAIL_APP_PASSWORD)
        smtp.send_message(msg)


try:
    init_db()
except Exception as db_boot_err:
    print(f"[Startup DB Warning] {db_boot_err}")


@app.route("/")
def index():
    mosaic_dir = os.path.join(app.static_folder, "mosaic")
    try:
        mosaic_images = [
            f
            for f in os.listdir(mosaic_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif"))
        ]
    except Exception:
        mosaic_images = []
    weekly_champion = None
    try:
        state = sync_and_get_contest_state()
        weekly_champion = state.get("weekly_champion")
    except Exception as champ_err:
        print(f"[Champion Load Warning] {champ_err}")
    return render_template("index.html", mosaic_images=mosaic_images, weekly_champion=weekly_champion)

@app.route("/api/register/send-code", methods=["POST"])
def register_send_code():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    caregiver_role = (data.get("caregiver_role") or "").strip()

    if not first_name or not last_name or not email:
        return jsonify({"ok": False, "error": "First name, last name, and email are required."}), 400

    display_name = username or f"{first_name} {last_name[0]}."
    code = f"{random.randint(100000, 999999)}"
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=20)
    temp_hash = generate_password_hash("Harbor2026")

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, is_verified FROM harbor_members WHERE email = %s;", (email,))
            existing = cur.fetchone()
            if existing and existing["is_verified"]:
                return jsonify({"ok": False, "error": "An account with this email is already registered."}), 409

            if existing:
                cur.execute(
                    """
                    UPDATE harbor_members
                    SET username = %s,
                        display_name = %s,
                        caregiver_role = %s,
                        verification_code = %s,
                        code_expires_at = %s
                    WHERE email = %s;
                    """,
                    (username, display_name, caregiver_role, code, expires_at, email),
                )
            else:
                cur.execute(
                    """
                    INSERT INTO harbor_members
                        (username, display_name, email, password_hash, caregiver_role, is_verified, is_approved, verification_code, code_expires_at)
                    VALUES (%s, %s, %s, %s, %s, FALSE, FALSE, %s, %s);
                    """,
                    (username, display_name, email, temp_hash, caregiver_role, code, expires_at),
                )
        conn.commit()
    finally:
        conn.close()

    send_harbor_email(
        to_address=email,
        subject="Your 6-Digit Verification Code — The Harbor (shareyourwalk.com)",
        body_text=(
            f"Hi {first_name},\n\n"
            f"Welcome to The Harbor! Enter this 6-digit code to verify your email address:\n\n"
            f"    {code}\n\n"
            f"This code expires in 20 minutes.\n\n"
            f"Warmly,\nThe Harbor Team — shareyourwalk.com"
        ),
    )

    return jsonify({"ok": True, "message": f"6-digit confirmation code sent to {email}!"})


@app.route("/api/register/verify", methods=["POST"])
def register_verify():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    caregiver_role = (data.get("caregiver_role") or "").strip()
    bio = (data.get("bio") or "").strip()
    code = (data.get("code") or "").strip()

    if not email or not code:
        return jsonify({"ok": False, "error": "Please enter the 6-digit verification code sent to your email."}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, display_name, verification_code, code_expires_at
                FROM harbor_members
                WHERE email = %s;
                """,
                (email,),
            )
            member = cur.fetchone()
            if not member:
                return jsonify({"ok": False, "error": "Application record not found. Please start at Step 1."}), 404

            if member["verification_code"] != code:
                return jsonify({"ok": False, "error": "Incorrect 6-digit verification code. Please check your email."}), 400

            if member["code_expires_at"] and member["code_expires_at"] < datetime.now(timezone.utc):
                return jsonify({"ok": False, "error": "That verification code expired. Go back to Step 1 for a new code."}), 400

            final_display = username or (f"{first_name} {last_name[0]}." if first_name and last_name else member["display_name"])
            cur.execute(
                """
                UPDATE harbor_members
                SET username = %s,
                    display_name = %s,
                    caregiver_role = %s,
                    bio = %s,
                    is_verified = TRUE,
                    verification_code = NULL,
                    code_expires_at = NULL
                WHERE id = %s;
                """,
                (username, final_display, caregiver_role, bio, member["id"]),
            )
        conn.commit()
    finally:
        conn.close()

    if HARBOR_CONTACT_EMAIL:
        try:
            send_harbor_email(
                to_address=HARBOR_CONTACT_EMAIL,
                subject=f"[New Member Application] {first_name} {last_name} ({final_display})",
                body_text=(
                    f"A new caregiver verified their email and submitted a membership application on shareyourwalk.com:\n\n"
                    f"Name: {first_name} {last_name}\n"
                    f"Username: {username or '(none)'}\n"
                    f"Email: {email}\n"
                    f"Role: {caregiver_role}\n\n"
                    f"Caregiver Story / Note:\n{bio}\n"
                ),
            )
        except Exception as notify_err:
            print(f"[Admin Notify Warning] {notify_err}")

    return jsonify({"ok": True})


@app.route("/api/login", methods=["POST"])
def login_member():
    data = request.get_json(silent=True) or {}
    login_id = (data.get("login_id") or "").strip()
    password = data.get("password") or ""

    if not login_id or not password:
        return jsonify({"ok": False, "error": "Please enter your username/email and password."}), 400

    # Admin passphrase login support
    if MASTER_PIN and secrets.compare_digest(password, MASTER_PIN):
        session["member_id"] = 0
        session["member_name"] = login_id or "Anthony"
        session["is_admin"] = True
        return jsonify({"ok": True, "display_name": login_id or "Anthony", "is_admin": True})

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, display_name, password_hash, caregiver_role, is_verified, is_approved
                FROM harbor_members
                WHERE LOWER(email) = LOWER(%s) OR LOWER(username) = LOWER(%s) OR LOWER(display_name) = LOWER(%s)
                LIMIT 1;
                """,
                (login_id, login_id, login_id),
            )
            member = cur.fetchone()
    finally:
        conn.close()

    if not member or not check_password_hash(member["password_hash"], password):
        return jsonify({"ok": False, "error": "Incorrect username/email or password."}), 401

    if not member["is_verified"]:
        return jsonify({"ok": False, "error": "Please finish verifying your email address first."}), 403

    if not member["is_approved"]:
        return jsonify({"ok": False, "error": "Your application is currently pending 24-hour Admin approval."}), 403

    session["member_id"] = member["id"]
    session["member_name"] = member["display_name"]

    return jsonify(
        {
            "ok": True,
            "display_name": member["display_name"],
            "caregiver_role": member["caregiver_role"],
        }
    )

@app.route("/api/change-password", methods=["POST"])
def change_password():
    member_id = session.get("member_id")
    if not member_id:
        return jsonify({"ok": False, "error": "Please sign in first."}), 401

    data = request.get_json(silent=True) or {}
    current_password = data.get("current_password") or ""
    new_password = (data.get("new_password") or "").strip()

    if len(new_password) < 6:
        return jsonify({"ok": False, "error": "New password must be at least 6 characters."}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT password_hash FROM harbor_members WHERE id = %s LIMIT 1;",
                (member_id,),
            )
            member = cur.fetchone()

            if not member or not check_password_hash(member["password_hash"], current_password):
                return jsonify({"ok": False, "error": "Current password is incorrect."}), 400

            new_hash = generate_password_hash(new_password)
            cur.execute(
                "UPDATE harbor_members SET password_hash = %s WHERE id = %s;",
                (new_hash, member_id),
            )
            conn.commit()
    finally:
        conn.close()

    return jsonify({"ok": True, "message": "Password updated successfully."})
@app.route("/api/admin/unlock", methods=["POST"])
def admin_unlock():
    data = request.get_json(silent=True) or {}
    entered_phrase = (data.get("passphrase") or "").strip()

    if not MASTER_PIN:
        return jsonify({"ok": False, "error": "MASTER_PIN is not configured on the server."}), 500

    if not secrets.compare_digest(entered_phrase, MASTER_PIN):
        return jsonify({"ok": False, "error": "Incorrect Admin passphrase."}), 401

    session["is_admin"] = True
    return jsonify({"ok": True})


@app.route("/api/contact", methods=["POST"])
def contact_harbor():
    data = request.get_json(silent=True) or {}
    sender_name = (data.get("name") or "").strip()
    sender_email = (data.get("email") or "").strip()
    sender_phone = (data.get("phone") or "").strip()
    contact_pref = (data.get("contact_pref") or "Email only").strip()
    cause_designation = (data.get("cause_designation") or "").strip()

    if not sender_name or not sender_email:
        return jsonify({"ok": False, "error": "Name and email are required."}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO harbor_inquiries
                    (sender_name, sender_email, sender_phone, contact_pref, inquiry_type, cause_designation, message)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    sender_name,
                    sender_email,
                    sender_phone,
                    contact_pref,
                    "Guests & Contributors",
                    cause_designation,
                    cause_designation or "Contributor / Sponsor Outreach",
                ),
            )
        conn.commit()
    finally:
        conn.close()

    if HARBOR_CONTACT_EMAIL:
        send_harbor_email(
            to_address=HARBOR_CONTACT_EMAIL,
            subject=f"[The Harbor Contributor Inquiry] from {sender_name}",
            body_text=(
                f"New Guests & Contributors inquiry from shareyourwalk.com:\n\n"
                f"Name: {sender_name}\n"
                f"Email: {sender_email}\n"
                f"Phone: {sender_phone or 'Not provided'}\n"
                f"Preferred Contact Method: {contact_pref}\n"
                f"Cause / Note:\n{cause_designation or 'None'}\n"
            ),
        )

    return jsonify({"ok": True})


EASTERN_TZ = ZoneInfo("America/New_York")


def _contest_schedule_info(now_et=None):
    """Determine the current week_key and active/between-round phase in Eastern Time."""
    now_et = now_et or datetime.now(EASTERN_TZ)
    # Shift back 8 hours on Sunday so Sunday 12:00 AM - 7:59 AM finishes the prior Saturday celebration
    shifted = now_et - timedelta(hours=8)
    # Python weekday: Mon=0 .. Sun=6 -> make Sunday=0, Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6
    days_since_sun = (shifted.weekday() + 1) % 7
    week_sun_date = (shifted - timedelta(days=days_since_sun)).date()
    week_key = week_sun_date.isoformat()

    wd = now_et.weekday()  # Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
    mins = now_et.hour * 60 + now_et.minute

    # Determine which rounds have passed their 8:15 PM (1215 min) lock cutoff
    past_mon_815 = (wd in (1, 2, 3, 4, 5)) or (wd == 0 and mins >= 1215) or (wd == 6 and mins < 480)
    past_wed_815 = (wd in (3, 4, 5)) or (wd == 2 and mins >= 1215) or (wd == 6 and mins < 480)
    past_fri_815 = (wd == 5) or (wd == 4 and mins >= 1215) or (wd == 6 and mins < 480)
    past_sat_815 = (wd == 5 and mins >= 1215) or (wd == 6 and mins < 480)

    if wd == 6 and mins >= 480:
        phase = {"code": "MON", "status": "OPEN", "label": "Round 1 (Monday) • Open Now", "sub": "Closes Monday at 8:00 PM ET • Winner locks at 8:15 PM"}
    elif wd == 0 and mins < 1200:
        phase = {"code": "MON", "status": "OPEN", "label": "Round 1 (Monday) • Open Now", "sub": "Closes Tonight at 8:00 PM ET • Winner locks at 8:15 PM"}
    elif wd == 0 and mins < 1215:
        phase = {"code": "MON", "status": "TALLYING", "label": "Round 1 (Monday) • Tallying Votes", "sub": "Monday Winner reveals at 8:15 PM ET!"}
    elif (wd == 0 and mins >= 1215) or (wd == 1 and mins < 480):
        phase = {"code": "MON", "status": "LOCKED_WAIT", "label": "Monday Winner Locked • Pushed to Saturday Run-Off!", "sub": "Round 2 (Wednesday) opens Tuesday at 8:00 AM ET"}
    elif wd == 1 and mins >= 480:
        phase = {"code": "WED", "status": "OPEN", "label": "Round 2 (Wednesday) • Open Now", "sub": "Closes Wednesday at 8:00 PM ET • Winner locks at 8:15 PM"}
    elif wd == 2 and mins < 1200:
        phase = {"code": "WED", "status": "OPEN", "label": "Round 2 (Wednesday) • Open Now", "sub": "Closes Tonight at 8:00 PM ET • Winner locks at 8:15 PM"}
    elif wd == 2 and mins < 1215:
        phase = {"code": "WED", "status": "TALLYING", "label": "Round 2 (Wednesday) • Tallying Votes", "sub": "Wednesday Winner reveals at 8:15 PM ET!"}
    elif (wd == 2 and mins >= 1215) or (wd == 3 and mins < 480):
        phase = {"code": "WED", "status": "LOCKED_WAIT", "label": "Wednesday Winner Locked • Pushed to Saturday Run-Off!", "sub": "Round 3 (Friday) opens Thursday at 8:00 AM ET"}
    elif wd == 3 and mins >= 480:
        phase = {"code": "FRI", "status": "OPEN", "label": "Round 3 (Friday) • Open Now", "sub": "Closes Friday at 8:00 PM ET • Winner locks at 8:15 PM"}
    elif wd == 4 and mins < 1200:
        phase = {"code": "FRI", "status": "OPEN", "label": "Round 3 (Friday) • Open Now", "sub": "Closes Tonight at 8:00 PM ET • Winner locks at 8:15 PM"}
    elif wd == 4 and mins < 1215:
        phase = {"code": "FRI", "status": "TALLYING", "label": "Round 3 (Friday) • Tallying Votes", "sub": "Friday Winner reveals & Saturday Run-Off unlocks at 8:15 PM ET!"}
    elif (wd == 4 and mins >= 1215) or (wd == 5 and mins < 1200):
        phase = {"code": "SAT", "status": "OPEN", "label": "🏆 Saturday Run-Off • Vote for Weekly Champion!", "sub": "All 3 Mon/Wed/Fri winners are live! Closes Saturday at 8:00 PM ET"}
    elif wd == 5 and mins < 1215:
        phase = {"code": "SAT", "status": "TALLYING", "label": "🏆 Saturday Run-Off • Tallying Final Votes", "sub": "Weekly Champion crowns at 8:15 PM ET!"}
    else:
        phase = {"code": "SAT", "status": "CHAMPION", "label": "👑 Weekly Champion Crowned!", "sub": "Featured on the Sign-In Screen • New week opens Sunday at 8:00 AM ET"}

    return {
        "week_key": week_key,
        "phase": phase,
        "locks": {
            "MON": past_mon_815,
            "WED": past_wed_815,
            "FRI": past_fri_815,
            "SAT": past_sat_815,
        },
    }


def sync_and_get_contest_state():
    """Lock finished rounds automatically and return full contest + champion state."""
    sched = _contest_schedule_info()
    week_key = sched["week_key"]
    phase = sched["phase"]
    locks = sched["locks"]

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Automatically lock Mon/Wed/Fri winners once past 8:15 PM ET
            for rcode in ("MON", "WED", "FRI"):
                if locks[rcode]:
                    cur.execute(
                        "SELECT id FROM harbor_pic_entries WHERE week_key = %s AND round_code = %s AND is_round_winner = TRUE LIMIT 1;",
                        (week_key, rcode),
                    )
                    if not cur.fetchone():
                        cur.execute(
                            """
                            SELECT id FROM harbor_pic_entries
                            WHERE week_key = %s AND round_code = %s
                            ORDER BY votes DESC, id ASC
                            LIMIT 1;
                            """,
                            (week_key, rcode),
                        )
                        top = cur.fetchone()
                        if top:
                            cur.execute("UPDATE harbor_pic_entries SET is_round_winner = TRUE WHERE id = %s;", (top["id"],))

            # Automatically crown Weekly Champion once Saturday 8:15 PM ET passes
            if locks["SAT"]:
                cur.execute(
                    "SELECT id FROM harbor_pic_entries WHERE week_key = %s AND is_weekly_champion = TRUE LIMIT 1;",
                    (week_key,),
                )
                if not cur.fetchone():
                    cur.execute(
                        """
                        SELECT id FROM harbor_pic_entries
                        WHERE week_key = %s AND is_round_winner = TRUE
                        ORDER BY votes DESC, id ASC
                        LIMIT 1;
                        """,
                        (week_key,),
                    )
                    champ = cur.fetchone()
                    if champ:
                        cur.execute("UPDATE harbor_pic_entries SET is_weekly_champion = TRUE WHERE id = %s;", (champ["id"],))

            conn.commit()

            # Fetch current round entries (for MON/WED/FRI)
            round_entries = []
            if phase["code"] in ("MON", "WED", "FRI"):
                cur.execute(
                    """
                    SELECT id, round_code, author_name, caption, image_url, votes, is_round_winner
                    FROM harbor_pic_entries
                    WHERE week_key = %s AND round_code = %s
                    ORDER BY votes DESC, id ASC;
                    """,
                    (week_key, phase["code"]),
                )
                round_entries = [dict(r) for r in cur.fetchall()]

            # Fetch Saturday Run-Off finalists (locked Mon/Wed/Fri winners)
            cur.execute(
                """
                SELECT id, round_code, author_name, caption, image_url, votes, is_weekly_champion
                FROM harbor_pic_entries
                WHERE week_key = %s AND is_round_winner = TRUE
                ORDER BY CASE round_code WHEN 'MON' THEN 1 WHEN 'WED' THEN 2 WHEN 'FRI' THEN 3 ELSE 4 END;
                """,
                (week_key,),
            )
            finalists = [dict(r) for r in cur.fetchall()]

            # Fetch most recently crowned Weekly Champion (stays live on sign-in screen all week!)
            cur.execute(
                """
                SELECT id, week_key, round_code, author_name, caption, image_url, votes
                FROM harbor_pic_entries
                WHERE is_weekly_champion = TRUE
                ORDER BY id DESC
                LIMIT 1;
                """
            )
            champ_row = cur.fetchone()
            weekly_champion = dict(champ_row) if champ_row else None
    finally:
        conn.close()

    return {
        "ok": True,
        "week_key": week_key,
        "phase": phase,
        "round_entries": round_entries,
        "finalists": finalists,
        "weekly_champion": weekly_champion,
    }


@app.route("/api/contest/state", methods=["GET"])
def get_contest_state():
    return jsonify(sync_and_get_contest_state())


@app.route("/api/contest/upload", methods=["POST"])
def upload_contest_photo():
    sched = _contest_schedule_info()
    phase = sched["phase"]
    if phase["code"] not in ("MON", "WED", "FRI") or phase["status"] != "OPEN":
        return jsonify({"ok": False, "error": f"Submissions are currently closed ({phase['label']})."}), 400

    photo = request.files.get("photo")
    caption = (request.form.get("caption") or "").strip() or "Shared from The Harbor"
    author_name = (request.form.get("author_name") or session.get("member_name") or "Harbor Member").strip()

    if not photo or not photo.filename:
        return jsonify({"ok": False, "error": "Please select a photo to upload."}), 400

    ext = os.path.splitext(secure_filename(photo.filename))[1].lower()
    if ext not in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
        return jsonify({"ok": False, "error": "Please upload a JPG, PNG, WEBP, or GIF image."}), 400

    upload_dir = os.path.join(app.static_folder, "uploads", "contest")
    os.makedirs(upload_dir, exist_ok=True)
    saved_name = f"{sched['week_key']}_{phase['code']}_{secrets.token_hex(6)}{ext}"
    photo.save(os.path.join(upload_dir, saved_name))
    image_url = f"/static/uploads/contest/{saved_name}"

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO harbor_pic_entries (week_key, round_code, author_name, caption, image_url, votes)
                VALUES (%s, %s, %s, %s, %s, 0);
                """,
                (sched["week_key"], phase["code"], author_name, caption, image_url),
            )
        conn.commit()
    finally:
        conn.close()

    return jsonify(sync_and_get_contest_state())


@app.route("/api/contest/vote", methods=["POST"])
def cast_contest_vote():
    data = request.get_json(silent=True) or {}
    entry_id = data.get("entry_id")
    voter_name = (data.get("voter_name") or session.get("member_name") or request.remote_addr or "guest").strip().lower()

    sched = _contest_schedule_info()
    phase = sched["phase"]
    if phase["status"] != "OPEN":
        return jsonify({"ok": False, "error": "Voting is currently closed while results finalize."}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id FROM harbor_pic_votes
                WHERE week_key = %s AND round_code = %s AND voter_key = %s;
                """,
                (sched["week_key"], phase["code"], voter_name),
            )
            if cur.fetchone():
                return jsonify({"ok": False, "error": "You already cast your vote for this round!"}), 409

            cur.execute(
                """
                INSERT INTO harbor_pic_votes (week_key, round_code, voter_key, entry_id)
                VALUES (%s, %s, %s, %s);
                """,
                (sched["week_key"], phase["code"], voter_name, entry_id),
            )
            cur.execute("UPDATE harbor_pic_entries SET votes = votes + 1 WHERE id = %s;", (entry_id,))
        conn.commit()
    finally:
        conn.close()

    return jsonify(sync_and_get_contest_state())


@app.route("/api/wall", methods=["GET", "POST"])
def serious_wall_api():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if request.method == "POST":
                data = request.get_json(silent=True) or {}
                category = (data.get("category") or "Question for the Wall").strip()
                topic = (data.get("topic") or "").strip()
                message = (data.get("message") or "").strip()
                author_name = (data.get("author_name") or session.get("member_name") or "A Fellow Caregiver").strip()
                if not topic or not message:
                    return jsonify({"ok": False, "error": "Topic and message are required."}), 400
                cur.execute(
                    """
                    INSERT INTO harbor_wall_posts (category, topic, message, author_name)
                    VALUES (%s, %s, %s, %s);
                    """,
                    (category, topic, message, author_name),
                )
                conn.commit()

            cur.execute("SELECT * FROM harbor_wall_posts ORDER BY id DESC LIMIT 50;")
            posts = [dict(r) for r in cur.fetchall()]
            for p in posts:
                cur.execute(
                    "SELECT id, author_name, reply_text FROM harbor_wall_replies WHERE post_id = %s ORDER BY id ASC;",
                    (p["id"],),
                )
                p["replies"] = [dict(rep) for rep in cur.fetchall()]
    finally:
        conn.close()

    return jsonify({"ok": True, "posts": posts})

@app.route("/api/wall/<int:post_id>", methods=["DELETE"])
def delete_serious_wall_post(post_id):
    is_admin = bool(session.get("is_admin"))
    member_name = (session.get("member_name") or "").strip().lower()

    if not is_admin and not member_name:
        return jsonify({"ok": False, "error": "Please sign in first."}), 401

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT author_name FROM harbor_wall_posts WHERE id = %s LIMIT 1;",
                (post_id,),
            )
            post = cur.fetchone()
            if not post:
                return jsonify({"ok": False, "error": "Post not found."}), 404

            post_author = (post["author_name"] or "").strip().lower()
            if not is_admin and post_author != member_name:
                return jsonify({"ok": False, "error": "You can only remove your own pinned posts."}), 403

            cur.execute("DELETE FROM harbor_wall_replies WHERE post_id = %s;", (post_id,))
            cur.execute("DELETE FROM harbor_wall_posts WHERE id = %s;", (post_id,))
            conn.commit()
    finally:
        conn.close()

    return jsonify({"ok": True})
@app.route("/api/wall/<int:post_id>/reply", methods=["POST"])
def reply_serious_wall(post_id):
    data = request.get_json(silent=True) or {}
    reply_text = (data.get("reply_text") or "").strip()
    author_name = (data.get("author_name") or session.get("member_name") or "Harbor Member").strip()
    if not reply_text:
        return jsonify({"ok": False, "error": "Reply cannot be empty."}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO harbor_wall_replies (post_id, author_name, reply_text) VALUES (%s, %s, %s);",
                (post_id, author_name, reply_text),
            )
        conn.commit()
    finally:
        conn.close()

    return jsonify({"ok": True})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)