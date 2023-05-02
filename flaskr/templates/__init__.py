from flask import Flask

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KET']='WDVBT54W23efg'

    return app