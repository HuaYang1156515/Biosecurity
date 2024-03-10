from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from connect import dbuser, dbpass, dbhost, dbport, dbname
from functools import wraps

def get_db_connection():
    try:
        # Create a connection object
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
    # app configuration and route definitions
    app.run(debug=True)


#hashing salt
from flask import Flask
from flask_hashing import Hashing

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'  
hashing = Hashing(app)

def hash_password(password):
    
    return hashing.hash_value(password, salt='*')  # 将 'some_salt_here' 替换为您的盐

def check_password(input_password, stored_hash):
     
    return hashing.check_value(stored_hash, input_password, salt='*')  # 将 'some_salt_here' 替换为您的盐

#home page
@app.route('/')
def home():
    return render_template('homepage.html')


#登录和注册
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 假设用户名和密码的表单字段分别为 'username' 和 'password'
        username = request.form['username']
        password = request.form['password']
        
        # 在这里您通常会包含验证用户名和密码的逻辑，
        # 比如查询数据库并检查哈希密码。
        # ...

        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 使用您的 hash_password 函数对密码进行哈希处理
        hashed_password = hash_password(password)
        
        # 在这里您会将新用户数据插入到数据库中。
        # ...

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
                # If there is no user_id in the session, redirect to login
                return redirect(url_for('login'))
            
            user_id = session['user_id']
            # Retrieve the role from the database based on the user_id
            # This requires a function or a database query to get the user's role
            user_role = get_user_role(user_id)
            
            if user_role is None or user_role != role:
                # If the role does not match or there is no role found, abort with a 403 error
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
    connection = get_db_connection()  # Make sure this function is properly defined to open a database connection
    try:
        with connection.cursor() as cursor:
            # If your users table has a field 'role' that references 'role_id' in the roles table
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
        # 如果用户未登录，则重定向到登录页面
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    if request.method == 'POST':
        # 检索表单数据
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        # ... 根据需要包括其他字段

        try:
            with conn.cursor() as cursor:
                # 更新数据库中用户的个人资料信息
                sql = "UPDATE users SET first_name=%s, last_name=%s WHERE user_id=%s"
                cursor.execute(sql, (first_name, last_name, user_id))
                conn.commit()
                flash('个人资料更新成功！', 'success')
        except Exception as e:
            flash(f'发生错误：{e}', 'error')
        finally:
            conn.close()

    # 获取当前用户的个人资料信息以显示
    user_profile = None
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            user_profile = cursor.fetchone()
    finally:
        conn.close()

    # 渲染个人资料模板，传递用户的个人资料信息
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

#guide.html page

@app.route('/guide')
def guide():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ocean_guide")
    guide_items = cursor.fetchall()
    conn.close()
    return render_template('guide.html', guide_items=guide_items)

@app.route('/guide/<int:id>')
def guide_detail(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ocean_guide WHERE id = %s", (id,))
    item_details = cursor.fetchone()
    conn.close()
    return render_template('guide_detail.html', item=item_details)

def get_all_pests_from_db():
    conn = get_db_connection()  # 确保此函数连接到您的数据库
    pests = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM ocean_guide")  # 根据实际表名和列调整
            pests = cursor.fetchall()  # 检索所有记录
    except Exception as e:
        print(f"An error occurred while fetching pests: {e}")
    finally:
        conn.close()
    return pests

def get_pest_detail_from_db(pest_id):
    conn = get_db_connection()  # 确保此函数连接到您的数据库
    pest = None
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM ocean_guide WHERE id = %s", (pest_id,))  # 根据实际表名和列调整
            pest = cursor.fetchone()  # 检索一条记录
    except Exception as e:
        print(f"An error occurred while fetching pest details: {e}")
    finally:
        conn.close()
    return pest

