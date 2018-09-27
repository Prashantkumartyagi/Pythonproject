from flask import current_app as app, flash, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, login_required, logout_user
from flask import Flask,request, render_template, redirect, url_for
from datetime import datetime
from flask import Response
from flask import jsonify
import urllib.request
import hashlib
import sys
from flask_cors import CORS, cross_origin
from urllib.request import Request, urlopen
from sqlalchemy import func, create_engine
import json
from collections import Counter
#-----------  mongo file ----module-----
from pymongo import MongoClient
from bson import ObjectId

#-------------- mongo file -----module end--
#date time
import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
client = MongoClient('localhost', 27017)
engine = create_engine("postgresql://postgres:@localhost/analytics", isolation_level="AUTOCOMMIT")
mydb = client.analytics
db=SQLAlchemy(app)


def user_loader(user_id):
    return SessionUser.find_by_session_id(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    if session.get('logged_in'):
        # prevent flashing automatically logged out message
        del session['logged_in']
    flash('You have successfully logged yourself out.')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if app.current_user.is_authenticated:  # already logged in
        return redirect('/home')
    if request.method == 'POST':
        user = SessionUser.find_by_session_id(request.data['user_id'])
        if user:
            login_user(user)
            session['logged_in'] = True
            return redirect('/home')
        flash('That user was not found in the database.')
    if session.get('logged_in'):
        flash('You have been automatically logged out.')
        del session['logged_in']
    return render_template('/login.html')

@app.route('/home')
@login_required
def home():
    return 'You are logged in as {0}.'.format(app.current_user.id)

def user_loader(id):
    # print(id)  # try printing current user's id to check.
    user = SessionUser.find_by_session_id(id) #hits the database
    if user is None:
        flash('You have been automatically logged out')
    return user

if __name__=="__main__":
    app.run(debug=True,host='10.0.0.87',port=8080)