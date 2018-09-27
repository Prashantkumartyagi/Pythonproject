from flask import Flask,request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
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


class Signup(db.Model):
    __tablename__='signup'
    id=db.Column('id',db.Integer,primary_key=True)
    name=db.Column('username',db.String)
    email=db.Column('email',db.String)
    password=db.Column('password',db.String)
    active = db.Column('active', db.Integer)
    mobile = db.Column('mobile', db.String)
    skype_id = db.Column('skype_id', db.String)
    address_1 = db.Column('address_1', db.String)
    address_2 = db.Column('address_2', db.String)
    city = db.Column('city', db.String)
    state = db.Column('state', db.String)
    zip = db.Column('zip', db.String)
    gender = db.Column('gender', db.String)
    dob = db.Column('dob', db.String)
    merital_status = db.Column('merital_status', db.String)
    company_name = db.Column('company_name', db.String)
    company_address = db.Column('company_address', db.String)


    def __init__(self,name,email,password):
        self.name = name
        self.id = id
        self.email = email
        self.password = password
        self.mobile = mobile
        self.skype_id = skype_id
        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.state = state
        self.zip = zip
        self.gender = gender
        self.dob = dob
        self.merital_status = merital_status

#*********** Login start******
@app.route("/login", methods=['POST','GET'])
def login_form():
    error = ""
    alert = ""
    userRequired = {
        'type': 'validation',
        'message': '',
        'status': 0
    }
    userData = {
        'name': '',
        'email':'' ,
        'phone': '',
        'password': ''
    }
    if request.method == 'POST':
        jsonData = request.get_json(force=True)
        email =jsonData['email']
        password = jsonData['password']
        password = hashlib.sha224(password.encode('utf-8')).hexdigest()

        if email == "" :
            userRequired = {
                'type': 'validation',
                'message': 'Email is required',
                'status': 0
            }
        if password == "":
            userRequired = {
                'type': 'validation',
                'message': 'password is required',
                'status': 0
            }

        if email !="" and password !="":
            #record_id = mydb.users.insert(userData)
            record_id = mydb.users.find_one({"email":email, "password":password});
            if(record_id):
                userSignupSuccess = {
                    'type': 'login',
                    'status': 1,
                    'message': 'user login successfully',
                    'userdata':str(record_id)
                }
                return jsonify(userSignupSuccess)
                sys.exit()
            else:
                userRequired = {
                    'type': 'login',
                    'message': 'Login Fail! Email or Password is wrong',
                    'status': 0
                }
                return jsonify(userRequired)
                sys.exit()
        else:

            return jsonify(userRequired)
            sys.exit()
    return jsonify(status)

if __name__=="__main__":
    app.run(debug=True,host='10.0.0.87',port=8080)

#*********** Login End******