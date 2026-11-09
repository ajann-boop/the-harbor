import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Supabase Connection String pulled safely from Render environment variables
DATABASE_URL = os.environ.get('DATABASE_URL', '')

def init_db():
    """Creates your structural database tables in Supabase if they don't exist yet"""
    if not DATABASE_URL:
        print("Warning: DATABASE_URL is not set.")
        return
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Create table for Membership Applications
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id SERIAL PRIMARY KEY,
                situation_badges TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Supabase database initialized successfully.")
    except Exception as e:
        print(f"Database initialization error: {e}")

# Run database setup on startup
init_db()

def fetch_pending_applications():
    """Queries Supabase for all pending caregiver profiles and creates HTML list elements"""
    if not DATABASE_URL:
        return "<li>Database connection not configured.</li>"
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, situation_badges, created_at FROM applications WHERE status = 'pending' ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not rows:
            return "<li>No pending membership applications at this moment.</li>"
            
        html_output = ""
        for row in rows:
            app_id = row[0]
            badges = row[1]
            date_submitted = row[2].strftime('%Y-%m-%d %H:%M') if row[2] else "Recent"
            
            html_output += f"""
            <li style="padding: 10px; margin-bottom: 8px; background: #eef2f7; border-left: 4px solid #3498db; list-style: none;">
                <strong>Application #{app_id}</strong> [{date_submitted}]<br>
                <span style="font-size: 1.1em;">Selected Badges: {badges}</span>
                <div style="margin-top: 5px;">
                    <a href="/admin-action?action=approve&id={app_id}" style="color: green; margin-right: 15px; text-decoration: none; font-weight: bold;">[ Approve ]</a>
                    <a href="/admin-action?action=deny&id={app_id}" style="color: red; text-decoration: none;">[ Deny ]</a>
                </div>
            </li>
            """
        return html_output
    except Exception as e:
        return f"<li>Error loading applications from Supabase: {e}</li>"

@app.route('/')
def index():
    return render_template('harbour.html')

@app.route('/submit-application', methods=['POST'])
def submit_application():
    """Captures caregiver badge submissions from the frontend and saves them to Supabase"""
    badges_str = request.form.get('badges_text', 'General Caregiver')
    
    if DATABASE_URL:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO applications (situation_badges) VALUES (%s)",
                (badges_str,)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error saving application to database: {e}")
            
    return redirect(url_for('index'))

@app.route('/admin-login')
def admin_login():
    error = request.args.get('error', '')
    error_html = f'<p style="color: red;">{error}</p>' if error else ''
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>The Harbor - Admin Portal</title>
        <style>
            body {{ font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f4f7f6; }}
            .login-card {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; }}
            input[type="password"] {{ padding: 10px; width: 80%; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }}
            button {{ background: #2b5c8f; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="login-card">
            <h2>Sanctuary Access Portal</h2>
            {error_html}
            <form method="POST" action="/admin-verify">
                <input type="password" name="admin_pin" placeholder="Enter Master Admin PIN" required autocomplete="off">
                <br><br>
                <button type="submit">Verify Access</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route('/admin-verify', methods=['POST'])
def admin_verify():
    admin_pin_input = request.form.get('admin_pin', '')
    MASTER_PIN = "4321"
    
    if admin_pin_input == MASTER_PIN:
        return redirect(url_for('admin_command_center', pin=MASTER_PIN))
    else:
        return redirect(url_for('admin_login', error="Invalid Security PIN. Access Denied."))

@app.route('/admin')
def admin_command_center():
    user_pin = request.args.get('pin', '')
    MASTER_PIN = "4321"
    
    if user_pin != MASTER_PIN:
        return redirect(url_for('admin_login'))
        
    live_apps_html = fetch_pending_applications()
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Sanctuary Admin Command Center</title>
    </head>
    <body style="font-family: sans-serif; padding: 20px; background: #f9f9f9;">
        <h2>Sanctuary Admin Command Center</h2>
        <p>Welcome back, Administrator. Full root access granted (Powered by Supabase).</p>
        
        <hr style="margin: 20px 0;">
        
        <h3>Pending Membership Applications</h3>
        <ul>
            {live_apps_html}
        </ul>
        
        <p style="margin-top: 30px;"><a href="/">[ Return to Public Home ]</a></p>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)