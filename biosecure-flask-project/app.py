from flask import Flask, request, redirect, url_for, render_template, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import re

app = Flask(__name__)
app.secret_key = 'comp639'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Assuming there's a User class that complies with Flask-Login requirements
class User:
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    # Required for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Your user loading logic here, returning a User object
        pass

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='biosecurity'
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'], user.get('role', 'User'))  # Adjust based on your User model
            login_user(user_obj)
            return redirect(url_for('home'))
        else:
            return "Login failed. Please check your credentials.", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']  # Added collection from form
        first_name = request.form['first_name']  # Added collection from form
        last_name = request.form['last_name']  # Added collection from form

        if len(password) < 8 or not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            return "Password criteria not met", 400

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            db.close()
            return "Username already taken", 400
        
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
                       (username, hashed_password, email, first_name, last_name))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/')
def home():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM mariners")  # Adjust your query as needed
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('home.html', data=data)  # Pass data to your template, if needed

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                return redirect(url_for('login', next=request.url))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/mariner_profile')
@login_required
@role_required('Mariner')
def mariner_profile():
    # Mariner profile management logic
    return render_template('mariner_profile.html')

if __name__ == '__main__':
    app.run(debug=True)
