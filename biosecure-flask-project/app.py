from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import os
from connect import dbuser, dbpass, dbhost, dbport, dbname
from functools import wraps

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


if __name__ == '__main__':
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'
    app.run(debug=True)


#hashing salt
from flask import Flask
from flask_hashing import Hashing

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'  
hashing = Hashing(app)
os.environ['HASH_SALT'] = '1234'

def hash_password(password):
    salt = os.environ.get('HASH_SALT', 'fallback_salt_if_not_set')
    return hashing.hash_value(password, salt=salt)  

def check_password(input_password, stored_hash):
    salt = os.environ.get('HASH_SALT', 'fallback_salt_if_not_set')
    return hashing.check_value(stored_hash, input_password, salt=salt)


#home page
@app.route('/')
def home():
    return render_template('homepage.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       
        username = request.form['username']
        password = request.form['password']
                
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('logout', 'info')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
         
        hashed_password = hash_password(password)
                
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html')


#different dashboard roles
from flask import session, abort, redirect, url_for

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if 'user_id' not in session:
                 
                return redirect(url_for('login'))
            
            user_id = session['user_id']
             
            user_role = get_user_role(user_id)
            
            if user_role is None or user_role != role:
                
                abort(403)
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/mariner_dashboard')
def mariner_dashboard():
    return render_template('mariner_dashboard.html')

@app.route('/staff_dashboard')
def staff_dashboard():
    return render_template('staff_dashboard.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

 
def get_user_role(user_id):
    connection = get_db_connection()   
    try:
        with connection.cursor() as cursor:
             
            sql = "SELECT roles.role_name FROM users JOIN roles ON users.role = roles.role_id WHERE users.user_id = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            return result['role_name'] if result else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        connection.close()

#profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in'):
         
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    if request.method == 'POST':
       
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        

        try:
            with conn.cursor() as cursor:
               
                sql = "UPDATE users SET first_name=%s, last_name=%s WHERE user_id=%s"
                cursor.execute(sql, (first_name, last_name, user_id))
                conn.commit()
                flash('success', 'success')
        except Exception as e:
            flash(f'error{e}', 'error')
        finally:
            conn.close()

     
    user_profile = None
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            user_profile = cursor.fetchone()
    finally:
        conn.close()

     
    return render_template('profile.html', profile=user_profile)

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

 

# Ocean Guide Routes
@app.route('/guide')
def guide():
    pests = get_all_pests_from_db()
    return render_template('guide.html', pests=pests)

@app.route('/guide/<int:pest_id>')
def guide_detail(pest_id):
    pest = get_pest_detail_from_db(pest_id)
    if pest:
        
        return render_template('guide_detail.html', pest=pest)
    else:
        flash('Pest not found', 'error')
        return redirect(url_for('guide'))


# Database query functions
def get_all_pests_from_db():
    conn = get_db_connection()
    pests = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM ocean_guide")   
            pests = cursor.fetchall()
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
            cursor.execute("SELECT * FROM ocean_guide WHERE id = %s", (pest_id,))
            pest = cursor.fetchone()
    except Exception as e:
        print(f"An error occurred while fetching pest details: {e}")
    finally:
        conn.close()
    return pest

if __name__ == '__main__':
    app.run(debug=True)