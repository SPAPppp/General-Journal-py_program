from flask import Blueprint, render_template

views=Blueprint('views', __name__)

# created home route for the website
@views.route('/')
def home():
    return render_template("home.html")