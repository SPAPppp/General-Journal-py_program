from flask import Blueprint, render_template

auth=Blueprint('auth', __name__)

# authentication routes for the website
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
def login():
    return render_template('logout.html')

@auth.route('/singup')
def login():
    return render_template('singup.html')