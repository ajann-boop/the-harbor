import os
import urllib.parse
import psycopg2
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Database Connection (Pulls automatically from Render PostgreSQL or falls back)
DATABASE_URL = os.environ.get('DATABASE_URL', 'your_copied_postgresql_connection_string_here')

def init_db():
    """Creates your structural database tables if they don't exist yet"""
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
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database initialization note: {e}")

# Run database setup on startup
init_db()

def fetch_pending_applications():
    """Queries PostgreSQL for all pending caregiver profiles and creates HTML list elements"""
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
            date_submitted = row[2].strftime('%Y-%m-%d %H:%M')
            
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
        return f"<li>Error loading applications from database: {e}</li>"

def render_admin_login(error_msg=""):
    """Generates the secure login page for the Admin Command Center"""
    error_html = f'<p style="color: red;">{error_msg}</p>' if error_msg else ''
    
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

class HarborServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        if path == '/admin-login':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(render_admin_login().encode('utf-8'))
            
        elif path == '/admin':
            # Secure Admin PIN check via query parameter (?pin=4321)
            user_pin = query_params.get('pin', [''])[0]
            MASTER_PIN = "4321"  # Your secret master admin PIN
            
            if user_pin != MASTER_PIN:
                self.send_response(302)
                self.send_header('Location', '/admin-login')
                self.end_headers()
                return
                
            # Fetch live applications from PostgreSQL
            live_apps_html = fetch_pending_applications()
            
            admin_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Sanctuary Admin Command Center</title>
            </head>
            <body style="font-family: sans-serif; padding: 20px; background: #f9f9f9;">
                <h2>Sanctuary Admin Command Center</h2>
                <p>Welcome back, Administrator. Full root access granted.</p>
                
                <hr style="margin: 20px 0;">
                
                <h3>Pending Membership Applications</h3>
                <ul>
                    {live_apps_html}
                </ul>
                
                <p style="margin-top: 30px;"><a href="/">[ Return to Public Home ]</a></p>
            </body>
            </html>
            """
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(admin_html.encode('utf-8'))
            
        else:
            # Default Public Home Route
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            home_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head><title>The Harbor - Sanctuary Network</title></head>
            <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h1>Welcome to The Harbor</h1>
                <p>An All-Abilities & Inclusive Family Network</p>
                <br>
                <a href="/admin-login">Admin Portal</a>
            </body>
            </html>
            """
            self.wfile.write(home_html.encode('utf-8'))

    def do_POST(self):
        if self.path == '/admin-verify':
            content_length = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_length).decode('utf-8')
            post_data = urllib.parse.parse_qs(post_body)
            
            admin_pin_input = post_data.get('admin_pin', [''])[0]
            MASTER_PIN = "4321"
            
            if admin_pin_input == MASTER_PIN:
                # Redirect securely with embedded PIN token
                self.send_response(302)
                self.send_header('Location', f'/admin?pin={MASTER_PIN}')
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(render_admin_login("Invalid Security PIN. Access Denied.").encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), HarborServerHandler)
    print(f"Server running on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    run()