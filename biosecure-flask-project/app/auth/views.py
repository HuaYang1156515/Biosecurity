from . import auth_blueprint

@auth_blueprint.route('/login')
def login():
    # login logic here
    return "Login Page"
