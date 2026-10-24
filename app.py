import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for, session, send_from_directory
from authlib.integrations.flask_client import OAuth
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

app = Flask(__name__)
app.secret_key = 'harbor_secure_session_key'

serializer = URLSafeTimedSerializer(app.secret_key)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ADMIN_EMAIL = "a.s.jannuzzi@gmail.com"

app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID', 'your-google-client-id.apps.googleusercontent.com')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect('harbor.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            screen_name TEXT,
            group_category TEXT DEFAULT 'Community',
            is_donor INTEGER DEFAULT 0,
            anonymous_donor INTEGER DEFAULT 0,
            donation_amount REAL DEFAULT 0.0,
            hide_amount INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            is_verified INTEGER DEFAULT 0,
            photo_filename TEXT,
            facebook_link TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contest_photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            filename TEXT NOT NULL,
            votes INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('harbor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, screen_name, group_category, is_donor, anonymous_donor, donation_amount, hide_amount, is_admin, status, is_verified, photo_filename, facebook_link FROM users')
    users = cursor.fetchall()
    
    cursor.execute('SELECT id, title, filename, votes FROM contest_photos ORDER BY votes DESC')
    photos = cursor.fetchall()
    
    cursor.execute('SELECT id, title, filename, votes FROM contest_photos ORDER BY votes DESC LIMIT 1')
    winner = cursor.fetchone()
    conn.close()
    return render_template('harbour.html', users=users, photos=photos, winner=winner)
    
    logged_in_email = session.get('user_email')
    is_admin = session.get('is_admin', 0)
    
    return render_template('harbour.html', users=users, photos=photos, winner=winner, logged_in_email=logged_in_email, is_admin=is_admin)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/authorize')
def google_authorize():
    token = google.authorize_access_token()
    resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')
    user_info = resp.json()
    
    email = user_info.get('email').strip().lower()
    name = user_info.get('name', 'Google User')
    
    conn = sqlite3.connect('harbor.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    
    is_admin = 1 if email == ADMIN_EMAIL else 0
    status = 'approved' if is_admin else 'pending'
    
    if not user:
        cursor.execute('''
            INSERT INTO users (name, email, group_category, is_donor, anonymous_donor, donation_amount, hide_amount, is_admin, status, is_verified) 
            VALUES (?, ?, ?, 0, 0, 0.0, 0, ?, ?, 1)
        ''', (name, email, 'Community' if not is_admin else 'Family', is_admin, status))
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
    
    conn.close()
    
    session['user_email'] = user[2]
    session['is_admin'] = 1 if user[2] == ADMIN_EMAIL else user[9]
    flash(f'Successfully signed in via Google as {name}!')
    return redirect(url_for('index'))

@app.route('/join', methods=['POST'])
def join_network():
    name = request.form.get('name')
    email = request.form.get('email').strip().lower()
    group_category = request.form.get('group_category', 'Community')
    is_donor = 1 if request.form.get('is_donor') else 0
    anonymous_donor = 1 if request.form.get('anonymous_donor') else 0
    donation_amount = float(request.form.get('donation_amount') or 0.0)
    hide_amount = 1 if request.form.get('hide_amount') else 0
    facebook_link = request.form.get('facebook_link')
    
    is_admin = 1 if email == ADMIN_EMAIL else 0
    status = 'approved' if is_admin else 'pending'
    is_verified = 1 if is_admin else 0
    
    photo_filename = None
    file = request.files.get('photo')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo_filename = filename

    if name and email:
        try:
            conn = sqlite3.connect('harbor.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, email, group_category, is_donor, anonymous_donor, donation_amount, hide_amount, is_admin, status, is_verified, photo_filename, facebook_link) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, group_category, is_donor, anonymous_donor, donation_amount, hide_amount, is_admin, status, is_verified, photo_filename, facebook_link))
            conn.commit()
            conn.close()
            return render_template('harbour.html', users=users, photos=photos, winner=winner)
            token = serializer.dumps(email, salt='email-verify-salt')
            verify_url = url_for('verify_email', token=token, _external=True)
            
            flash(f'Registration successful! [Dev Mode Verification Link]: Click here to verify your email -> {verify_url}')
        except sqlite3.IntegrityError:
            flash('This email is already registered on the network.')

    return redirect(url_for('index'))

@app.route('/verify/<token>')
def verify_email(token):
    try:
        email = serializer.loads(token, salt='email-verify-salt', max_age=86400)
        conn = sqlite3.connect('harbor.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_verified = 1 WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        flash('Email verified successfully! Your account is now pending final admin review.')
    except (SignatureExpired, BadSignature):
        flash('The verification link is invalid or has expired.')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email').strip().lower()
    
    if email:
        conn = sqlite3.connect('harbor.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            if user[11] == 0 and user[9] != 1:
                flash('Please verify your email address before signing in (check your registration confirmation link).')
            else:
                session['user_email'] = user[2]
                session['is_admin'] = 1 if user[2] == ADMIN_EMAIL else user[9]
                flash(f'Welcome back, {user[3] or user[1]}!')
        else:
            flash('Email not found. Please join the network first.')

    return redirect(url_for('index'))

@app.route('/admin/upload-contest-photo', methods=['POST'])
def upload_contest_photo():
    if session.get('is_admin'):
        title = request.form.get('title')
        file = request.files.get('photo')
        if title and file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            conn = sqlite3.connect('harbor.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO contest_photos (title, filename, votes) VALUES (?, ?, 0)', (title, filename))
            conn.commit()
            conn.close()
            flash('Contest photo uploaded successfully!')
        else:
            flash('Please provide a title and a valid image file.')
    else:
        flash('Unauthorized action.')
    return redirect(url_for('index'))

@app.route('/vote/<int:photo_id>', methods=['POST'])
def vote_photo(photo_id):
    if session.get('user_email'):
        conn = sqlite3.connect('harbor.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE contest_photos SET votes = votes + 1 WHERE id = ?', (photo_id,))
        conn.commit()
        conn.close()
        flash('Vote recorded successfully!')
    else:
        flash('Please sign in to vote.')
    return redirect(url_for('index'))

@app.route('/admin/delete-photo/<int:photo_id>', methods=['POST'])
def delete_photo(photo_id):
    if session.get('is_admin'):
        conn = sqlite3.connect('harbor.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contest_photos WHERE id = ?', (photo_id,))
        conn.commit()
        conn.close()
        flash('Contest photo removed.')
    else:
        flash('Unauthorized action.')
    return redirect(url_for('index'))

@app.route('/update-profile', methods=['POST'])
def update_profile():
    email = session.get('user_email')
    screen_name = request.form.get('screen_name')
    facebook_link = request.form.get('facebook_link')
    
    photo_filename = None
    file = request.files.get('photo')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photo_filename = filename

    if email:
        conn = sqlite3.connect('harbor.db')
        cursor = conn.cursor()
        
        if screen_name and facebook_link and photo_filename:
            cursor.execute('UPDATE users SET screen_name = ?, facebook_link = ?, photo_filename = ? WHERE email = ?', (screen_name, facebook_link, photo_filename, email))
        elif screen_name and facebook_link:
            cursor.execute('UPDATE users SET screen_name = ?, facebook_link = ? WHERE email = ?', (screen_name, facebook_link, email))
        elif screen_name and photo_filename:
            cursor.execute('UPDATE users SET screen_name = ?, photo_filename = ? WHERE email = ?', (screen_name, photo_filename, email))
        elif facebook_link and photo_filename:
            cursor.execute('UPDATE users SET facebook_link = ?, photo_filename = ? WHERE email = ?', (facebook_link, photo_filename, email))
        elif screen_name:
            cursor.execute('UPDATE users SET screen_name = ? WHERE email = ?', (screen_name, email))
        elif facebook_link:
            cursor.execute('UPDATE users SET facebook_link = ? WHERE email = ?', (facebook_link, email))
        elif photo_filename:
            cursor.execute('UPDATE users SET photo_filename = ? WHERE email = ?', (photo_filename, email))
            
        conn.commit()
        conn.close()
        flash('Profile updated successfully!')
    return redirect(url_for('index'))

@app.route('/admin/approve/<int:user_id>', methods=['POST'])
def approve_user(user_id):
    if session.get('is_admin'):
        conn = sqlite3.connect('harbor.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET status = 'approved' WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        flash('Member verified and approved.')
    else:
        flash('Unauthorized action.')
    return redirect(url_for('index'))

@app.route('/admin/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('is_admin'):
        conn = sqlite3.connect('harbor.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        flash('Member removed from the network directory.')
    else:
        flash('Unauthorized action.')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
