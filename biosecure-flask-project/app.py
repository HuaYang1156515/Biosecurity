from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import os
import re  # Import regular expressions for password validation
from connect import dbuser, dbpass, dbhost, dbport, dbname
from functools import wraps

 

# Function to create a database connection
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=dbhost,   
            user=dbuser,    
            password=dbpass,  
            db=dbname,   
            port=int(dbport),   
            charset='utf8mb4',  
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None

# Function to check if a user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('You need to be logged in to view this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function




def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'Staff':
            flash('You do not have the required permissions to view this page.')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Assuming 'user_role' is stored in the session when the user logs in
        if 'user_role' not in session or session['user_role'] != 'Administrator':
            flash('You must be an administrator to view this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)
app.secret_key = os.urandom(24)


# Route for the homepage
@app.route('/')
def home():
    return render_template('homepage.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''SELECT users.user_id, users.username, users.password, roles.role_name
                          FROM users
                          INNER JOIN roles ON users.role_id = roles.role_id
                          WHERE username = %s''', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['username'] = user['username']
            session['user_role'] = user['role_name']
            session['user_id'] = user['user_id']

            # Print statement to check session contents after login
            print("Session at login:", dict(session))
            
            flash('You have successfully logged in.')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password')

    return render_template('login.html')






 
# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get registration form data
        username = request.form['username']
        password = request.form['password']
        # Assuming 'Mariner' role has a role_id of 1
        role_id = 1  # You might need to change this based on your roles table
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        if cursor.fetchone() is not None:
            flash('Username is already taken. Please choose a different one.')
            return redirect(url_for('register'))
        
        # Password validation
        if len(password) < 8 or not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
            flash('Password must be at least 8 characters long with a mix of letters and numbers.')
            return redirect(url_for('register'))
        
        # If validation is successful, hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Insert new user into the database with the role_id for 'Mariner'
        cursor.execute('INSERT INTO users (username, password, role_id) VALUES (%s, %s, %s)', 
                       (username, hashed_password, role_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Account created successfully!')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    print("Logging out user:", session.get('username'))
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have successfully logged out.')
    return redirect(url_for('home'))




"""@app.route('/dashboard')
@login_required
def dashboard():
    user_role = session.get('user_role')
    user_id = session.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    # For the mariner role, fetch from mariner_profiles and render mariner_dashboard
    if user_role == 'Mariner':
        cursor.execute("SELECT * FROM mariner_profiles WHERE user_id = %s", (user_id,))
        profile_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('mariner_dashboard.html', profile=profile_data)

    # For staff or administrator roles, fetch from staff_admin_profiles and render the appropriate dashboard
    elif user_role in ['Staff', 'Administrator']:
        cursor.execute("SELECT * FROM staff_admin_profiles WHERE user_id = %s", (user_id,))
        profile_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_role == 'Staff':
            return render_template('staff_dashboard.html', profile=profile_data)
        else: # user_role == 'Administrator'
            return render_template('admin_dashboard.html', profile=profile_data)
    
    else:
        # If role is not recognized, redirect to a default page or logout
        cursor.close()
        conn.close()
        flash('Unrecognized user role.')
        return redirect(url_for('logout'))"""

@app.route('/dashboard')
@login_required
def dashboard():
    print("Session at dashboard:", dict(session))
    
    # Convert the role to lowercase for case-insensitive comparison
    user_role = session.get('user_role', '').lower()  # Will handle None by converting it to an empty string
    user_id = session.get('user_id')
    
    if user_role not in ['mariner', 'staff', 'administrator']:
        print("Unrecognized role, redirecting to logout.")
        return redirect(url_for('logout'))
    
    # If role is recognized, fetch data and render dashboard
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if user_role == 'mariner':
            cursor.execute("SELECT * FROM mariner_profiles WHERE user_id = %s", (user_id,))
            profile_data = cursor.fetchone()
            return render_template('mariner_dashboard.html', profile=profile_data)
        elif user_role == 'staff':
            cursor.execute("SELECT * FROM staff_admin_profiles WHERE user_id = %s", (user_id,))
            profile_data = cursor.fetchone()
            return render_template('staff_dashboard.html', profile=profile_data)
        elif user_role == 'administrator':
            cursor.execute("SELECT * FROM staff_admin_profiles WHERE user_id = %s", (user_id,))
            profile_data = cursor.fetchone()
            return render_template('admin_dashboard.html', profile=profile_data)
    except Exception as e:
        print(f"Error fetching dashboard data: {e}")
        return redirect(url_for('logout'))
    finally:
        cursor.close()
        conn.close()

#profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session.get('user_id')
    user_role = session.get('user_role', '').capitalize()  # Ensure first letter is uppercase to match role names

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Assume you have form fields for first_name, last_name, email, and phone_number
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        try:
            # Update the user profile information.
            # You will need separate UPDATE statements for mariner_profiles and staff_admin_profiles based on user_role.
            if user_role == 'Mariner':
                cursor.execute('''UPDATE mariner_profiles SET first_name=%s, last_name=%s, email=%s, phone_number=%s 
                                  WHERE user_id=%s''',
                               (first_name, last_name, email, phone_number, user_id))
            else:
                cursor.execute('''UPDATE staff_admin_profiles SET first_name=%s, last_name=%s, email=%s, phone_number=%s 
                                  WHERE user_id=%s''',
                               (first_name, last_name, email, phone_number, user_id))
            conn.commit()
            flash('Profile updated successfully!')
        except Exception as e:
            conn.rollback()
            flash(f'Error updating profile: {e}')

    # Regardless of whether the request is GET or POST, display the current profile data
    try:
        if user_role == 'Mariner':
            cursor.execute("SELECT * FROM mariner_profiles WHERE user_id = %s", (user_id,))
        else:
            cursor.execute("SELECT * FROM staff_admin_profiles WHERE user_id = %s", (user_id,))

        profile_data = cursor.fetchone()
    except Exception as e:
        flash(f'Error fetching profile data: {e}')
        profile_data = {}

    cursor.close()
    conn.close()

    return render_template('profile.html', profile=profile_data, role=user_role)


#change_password
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        user_id = session.get('user_id')

        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match.')
            return redirect(url_for('change_password'))

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check the current password
        cursor.execute('SELECT password FROM users WHERE user_id = %s', (user_id,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], current_password):
            # Hash the new password
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')

            # Update the password in the database
            try:
                cursor.execute('UPDATE users SET password = %s WHERE user_id = %s', 
                               (hashed_password, user_id))
                conn.commit()
                flash('Your password has been updated.')
            except Exception as e:
                conn.rollback()
                flash(f'Error updating password: {e}')
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Current password is incorrect.')

    return render_template('change_password.html')







  # manage  
@app.route('/manage_mariners')
@login_required
@staff_required  # Make sure only staff can access this
def manage_mariners():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mariner_profiles')
    mariners = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage_mariners.html', mariners=mariners)
  
  #manage_guide
@app.route('/manage_guide')
@login_required
@staff_required  # This should be a role-check decorator for staff
def manage_guide():
    # Fetch ocean guide entries from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ocean_guide')
    guides = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage_guide.html', guides=guides)




@app.route('/admin_dashboard')
@login_required
@admin_required  # This is a placeholder for your role-check decorator
def admin_dashboard():
    # Perform actions specific to admin users
    return render_template('admin_dashboard.html')
   
   
   #manage_users
@app.route('/manage_users')
@login_required
@admin_required  # This should be a role-check decorator for admins
def manage_users():
    # Fetch all user profiles from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('manage_users.html', users=users)

  #full_guide_control
@app.route('/full_guide_control')
@login_required
@admin_required  # This should be a role-check decorator for admins
def full_guide_control():
    # Similar to manage_guide, but may include additional privileges
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ocean_guide')
    guides = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('full_guide_control.html', guides=guides)




# ocean guide
@app.route('/guide')
def guide():
   
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ocean_guide')
    guides = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('guide.html', guides=guides)

@app.route('/guide/<int:ocean_id>')
def guide_detail(ocean_id):
    # Fetch the specific guide entry from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ocean_guide WHERE ocean_id = %s', (ocean_id,))
    guide_detail = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # Check if guide entry exists
    if guide_detail is None:
        flash('The requested guide does not exist.')
        return redirect(url_for('guide'))

    return render_template('guide_detail.html', guide_detail=guide_detail)
 


if __name__ == '__main__':
    app.run(debug=True)

