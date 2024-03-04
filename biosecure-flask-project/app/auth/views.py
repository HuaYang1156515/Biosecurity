from . import auth_blueprint
from flask import render_template, request, redirect, url_for

from flask import render_template, request, redirect, url_for, flash
from . import auth_blueprint
from db import get_db

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        # Insert your database operation here
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')




@auth_blueprint.route('/login')
def login():
    # Logic for login view
    return render_template('auth/login.html')

# Add more auth related routes like register, logout etc.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Here you would get the username and password
        username = request.form['username']
        password = request.form['password']
        # You would then validate the credentials and log the user in
        # For now, let's just redirect to the home page
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collect form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Here you would insert the new user's data into the database
        # And then redirect to the login page
        return redirect(url_for('login'))
    return render_template('register.html')