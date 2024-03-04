from . import mariners_blueprint
from flask import render_template

@mariners_blueprint.route('/profile')
def profile():
    # Logic for displaying a mariner's profile
    return render_template('mariners/profile.html')

# Add more mariner related routes

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
