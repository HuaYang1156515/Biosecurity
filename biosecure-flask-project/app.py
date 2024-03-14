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

app = Flask(__name__)
app.secret_key = os.urandom(24)



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
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['username'] = user['username']
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
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have successfully logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)


#profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    if user_role == 'Mariner':
        profile_table = 'mariner_profiles'
    elif user_role in ['Staff', 'Administrator']:
        profile_table = 'staff_admin_profiles'
    else:
        flash('Invalid user role.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        # More fields and validation as needed
        # Update profile logic here using `profile_table` and form data
        pass
    else:
        # Fetch profile data
        cursor.execute(f"SELECT * FROM {profile_table} WHERE user_id = %s", (user_id,))
        profile_data = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return render_template('profile.html', profile=profile_data, role=user_role)







#dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch user role from session or database
    user_role = session.get('user_role')
    
    # Decide which dashboard to present based on the user's role
    if user_role == 'Mariner':
        return render_template('mariner_dashboard.html')
    elif user_role == 'Staff':
        return render_template('staff_dashboard.html')
    elif user_role == 'Administrator':
        return render_template('admin_dashboard.html')
    else:
        # If role is not recognized, redirect to a default page or logout
        flash('Unrecognized user role.')
        return redirect(url_for('logout'))
    



#different roles dashboard
  #mariner_dashboard
@app.route('/mariner_dashboard')
@login_required
def mariner_dashboard():
    # Perform actions specific to mariner users
    return render_template('mariner_dashboard.html')
 
     



@app.route('/staff_dashboard')
@login_required
@staff_required  # This is a placeholder for your role-check decorator
def staff_dashboard():
    # Perform actions specific to staff users
    return render_template('staff_dashboard.html')

  # manage  
@app.route('/manage_mariners')
@login_required
@staff_required  # Make sure only staff can access this
def manage_mariners():
    # Fetch mariner profiles from the database
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
 
 
#guide 
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
 
"""
#profile
 


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_id = session['user_id']
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return redirect(url_for('profile'))

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # Verify current password
                cursor.execute("SELECT password FROM users WHERE user_id=%s", (user_id,))
                user = cursor.fetchone()
                if not user or not check_password(current_password, user['password']):
                    flash('Current password is incorrect.', 'error')
                    return redirect(url_for('profile'))

                # Update the password in the database
                hashed_password = hash_password(new_password)
                cursor.execute("UPDATE users SET password=%s WHERE user_id=%s", (hashed_password, user_id))
                conn.commit()
                flash('Password updated successfully.', 'success')
        except Exception as e:
            flash(f'An error occurred while updating the password: {e}', 'error')
        finally:
            conn.close()
        return redirect(url_for('profile'))

    return render_template('change_password.html')

 



# Database query functions
def get_all_pests_from_db():
    conn = get_db_connection()
    pests = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
"""                SELECT g.ocean_id, g.common_name, i.image_url AS primary_image
                FROM ocean_guide g
                LEFT JOIN ocean_images i ON g.ocean_id = i.ocean_id AND i.is_primary = 1
            """   
"""            pests = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred while fetching pests: {e}")
    finally:
        conn.close()
    return pests


def get_pest_detail_from_db(pest_id):
    conn = get_db_connection()
    pest = None
    try:
        with conn.cursor() as cursor:
            # Fetch the main pest details along with the primary image path
            cursor.execute("""