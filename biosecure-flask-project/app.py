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
    # 在这里您应该处理登出逻辑，比如清除会话。
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 从表单中提取数据
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
@app.route('/dashboard')
def dashboard():
    # 检查用户是否已登录
    # 如果用户角色是 'mariner'，则重定向到 mariner_dashboard
    # 如果用户角色是 'staff'，则重定向到 staff_dashboard
    # 如果用户角色是 'admin'，则重定向到 admin_dashboard
    # 如果用户未登录或角色不被识别，则重定向到首页或登录页面
    return render_template('dashboard.html')

@app.route('/mariner_dashboard')
def mariner_dashboard():
    # 检查用户是否已登录，以及他们的角色是否是 'mariner'
    # 显示水手的仪表板，包括相关信息和选项
    # 如果用户不是水手或未登录，则适当地重定向
    return render_template('mariner_dashboard.html')

@app.route('/staff_dashboard')
def staff_dashboard():
    # 检查用户是否已登录，以及他们的角色是否是 'staff'
    # 显示员工仪表板，包括查看水手档案和管理指南的选项
    # 如果用户不是员工或未登录，则适当地重定向
    return render_template('staff_dashboard.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # 检查用户是否已登录，以及他们的角色是否是 'admin'
    # 显示管理员仪表板，包括完全访问选项
    # 如果用户不是管理员或未登录，则适当地重定向
    return render_template('admin_dashboard.html')
