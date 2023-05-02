from flask import Blueprint, render_template

auth=Blueprint('auth', __name__)

# authentication routes for the website
@auth.route('/login')
def login():
    return render_template('home.html')

@auth.route('/logout')
def logout():
    return render_template('logout.html')

@auth.route('/signup')
def signin():
    return render_template('singup.html')