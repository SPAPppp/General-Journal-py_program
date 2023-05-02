from flask import Blueprint, render_template

views=Blueprint('views', __name__)

# created home route for the website
@views.route('/home')
def home():
    return '<h1>Test</h1>'