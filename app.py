import os
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.utils import secure_filename
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.environ.get('DATABASE_PATH', 'applications.db')
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('FLASK_SECRET', 'change-this-secret')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        position = request.form.get('position', '').strip()
        location = request.form.get('location', '').strip()
        cover = request.form.get('cover', '').strip()
        auth_to_work = request.form.get('auth_to_work', 'no')

        if not name or not email or not position:
            flash('Please provide at least Name, Email and Position.', 'danger')
            return redirect(url_for('index'))

        cv_filename = None
        cv = request.files.get('cv')
        if cv and cv.filename != '':
            if allowed_file(cv.filename):
                filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{cv.filename}")
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                cv.save(save_path)
                cv_filename = filename
            else:
                flash('CV must be a PDF or Word document.', 'danger')
                return redirect(url_for('index'))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO applications
               (name, email, phone, position, location, cover, auth_to_work, cv_filename, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, email, phone, position, location, cover, auth_to_work, cv_filename, datetime.utcnow())
        )
        conn.commit()
        conn.close()

        return render_template('thanks.html', name=name, position=position)

    return render_template('index.html')

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
