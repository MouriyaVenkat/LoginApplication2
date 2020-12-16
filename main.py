from flask import Flask,render_template,url_for, redirect, request, session
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import xlsxwriter
from openpyxl import load_workbook
import re

app = Flask(__name__)
app.secret_key = 'JanaShree'

@app.route("/")
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        df = pd.read_excel("Database/login_credentials.xlsx",sheet_name = "Sheet1")
        users_cred = [tuple(x) for x in df.values]
        username = request.form['username']
        password = request.form['password']
        for name, pwd, email in users_cred:
            if name == username and pwd == password:
                msg = "Logged in successfully"
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for('home'))
        msg = "Invalid Credentials!"
    return render_template("login.html",msg=msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        df = pd.read_excel("Database/login_credentials.xlsx",sheet_name = "Sheet1")
        users_cred = [tuple(x) for x in df.values]
        account = False
        for name,pwd,eml in users_cred:
            if name == username:
                account=True
                break
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            df1 = pd.DataFrame({"username": [username], "password": [password], "email": [email]})
            df = df.append(df1, ignore_index=True)
            df.to_excel("Database/login_credentials.xlsx",index=False)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/login/home')
def home():
    return render_template("index.html")

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
    """
    df = pd.read_excel("Database/login_credentials.xlsx", sheet_name="Sheet1")
    df1 = pd.DataFrame({"username": ["user5"], "password": ["user5"], "email": ["user5@gmail.com"]})
    df = df.append(df1, ignore_index=True)
    print(df)
    df1 = pd.DataFrame({"username": ["user6"], "password": ["user6"], "email": ["user6@gmail.com"]})
    df = df.append(df1, ignore_index=True)
    print(df)
    users_cred = [tuple(x) for x in df.values]
    print(users_cred)
"""