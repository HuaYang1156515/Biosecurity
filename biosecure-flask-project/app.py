from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from connect import dbuser, dbpass, dbhost, dbport, dbname
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with your own secret key



# Database connection function
def get_db_connection():
    return pymysql.connect(host=dbhost,
                           user=dbuser,
                           password=dbpass,
                           db=dbname,
                           port=int(dbport),
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

# Hash a password
def hash_password(password):
    return generate_password_hash(password)

# Verify a password against a hash
def check_password(password, hash):
    return check_password_hash(hash, password)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
        conn.close()

        if user and check_password(password, user['password']):
            session['logged_in'] = True
            session['username'] = username
            flash('You were successfully logged in')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('homepage.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Dashboard logic goes here
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please login to view this page.')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function
