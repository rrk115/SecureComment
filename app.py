import os
import MySQLdb
import smtplib
import random
import string
from datetime import datetime
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash, send_file
from database import db_connect,inc_reg,admin_loginact,ins_loginact,ap_act,vp,ap_act1,vcact,profile_act,editact1,fbact1,vuact,vfact,vtcact,vtcact2,profile_2,vcact2,profile_4

import io
import json
import numpy as np
from sendmail import sendmail

# def db_connect():
#     _conn = MySQLdb.connect(host="localhost", user="root",
#                             passwd="root", db="assigndb")
#     c = _conn.cursor()

#     return c, _conn


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def FUN_root():
    return render_template("index.html")
    
@app.route("/admin.html")
def admin():
    return render_template("admin.html")

@app.route("/user.html")
def ins():
    return render_template("user.html")


@app.route("/increg.html")
def increg():
    return render_template("increg.html")



@app.route("/adminhome.html")
def adminhome():
    return render_template("adminhome.html")



@app.route("/ihome.html")
def ihome():
    data = vp()
    print(data)
    return render_template("ihome.html",data = data )





@app.route("/ap.html")
def ap():
    
    return render_template("ap.html")

@app.route("/vu.html")
def vu():
    data = vuact()
    print(data)
    return render_template("vu.html",data = data)


@app.route("/vf.html")
def vf():
    data = vfact()
    print(data)
    return render_template("vf.html",data = data)

@app.route("/vc.html")
def vc():
    user = session['username']
    data1 = vcact2(user)
    status = data1[0][5]
    print("0000000000")
    print(status)
    data = vcact(user,status)
    print(data)
    return render_template("vc.html",data = data)


@app.route("/profile.html")
def profile():
    username = session['username']
    data = profile_act(username)
    print(data)
    return render_template("profile.html",data = data)


@app.route("/vtc.html")
def vtc():
    data = vtcact()
    print(data)
    return render_template("vtc.html",data = data)



@app.route("/index")
def index():
    return render_template("index.html") 

@app.route("/fb.html")
def fb():
    return render_template("fb.html") 

@app.route("/vmm", methods = ['GET','POST'])
def vmm():
    user = request.args.get('user')
    post = request.args.get('post')
    pic = request.args.get('pic')
    
           
    return render_template("ap1.html",user = user,post=post,pic=pic)


@app.route("/profile1", methods = ['GET','POST'])
def profile1():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')
    mobile = request.args.get('mobile')
       
    return render_template("edit.html",username = username,password=password,email=email,mobile=mobile)


@app.route("/profile2", methods = ['GET','POST'])
def profile2():
    username = request.args.get('username')
    data = profile_2(username)
       
    return render_template("profile.html")


@app.route("/profile3", methods = ['GET','POST'])
def profile3():
    username = request.args.get('username')
    data = profile_4(username)
       
    return render_template("profile.html")

@app.route("/vtcact1", methods = ['GET','POST'])
def vtcact1():
    username = request.args.get('username')
    data = vtcact2(username)
    print(data)
    

    email = data[0][0]
    print(email)
    sendmail(email)  
    return render_template("vtc.html")
# -------------------------------Registration-----------------------------------------------------------------    



@app.route("/inceregact", methods = ['GET','POST'])
def inceregact():
   if request.method == 'POST':    
      
      status = inc_reg(request.form['username'],request.form['password'],request.form['email'],request.form['mobile'])
      
      if status == 1:
       return render_template("user.html",m1="sucess")
      else:
       return render_template("increg.html",m1="failed")

@app.route("/fbact", methods = ['GET','POST'])
def fbact():
   if request.method == 'POST':    
      username = session['username']
      status = fbact1(username,request.form['fb'])
      
      if status == 1:
       return render_template("fb.html",m1="sucess")
      else:
       return render_template("fb.html",m1="failed")

@app.route("/editact", methods = ['GET','POST'])
def editact():
   if request.method == 'POST':    
      
      status = editact1(request.form['username'],request.form['password'],request.form['email'],request.form['mobile'])
      
      if status == 1:
       return render_template("profile.html",m1="sucess")
      else:
       return render_template("profile.html",m1="failed")


@app.route("/apact", methods = ['GET','POST'])
def apact():
   if request.method == 'POST':    
      username = session['username']
      status = ap_act(username,request.form['post'],request.form['pic'])
      
      if status == 1:
       return render_template("ap.html",m1="sucess")
      else:
       return render_template("ap.html",m1="failed")
      


@app.route("/apact1", methods = ['GET','POST'])
def apact1():
   if request.method == 'POST':    
      username = session['username']
      status = ap_act1(username,request.form['user'],request.form['post'],request.form['pic'],request.form['cmnt'])
      
      if status == 1:
       return render_template("ap.html",m1="sucess")
      else:
       return render_template("ap.html",m1="failed")
      
# #-------------------------------ADD_END---------------------------------------------------------------------------
# # -------------------------------Loginact-----------------------------------------------------------------
@app.route("/adminlogact", methods=['GET', 'POST'])       
def adminlogact():
    if request.method == 'POST':
        status = admin_loginact(request.form['username'], request.form['password'])
        print(status)
        if status == 1:
            session['username'] = request.form['username']
            return render_template("adminhome.html", m1="sucess")
        else:
            return render_template("admin.html", m1="Login Failed")






@app.route("/inslogin", methods=['GET', 'POST'])
def inslogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        status = ins_loginact(username, password)
        print(status)

        if status == 1:
            session['username'] = username
            return render_template("ihome.html", m1="Success")
        else:
            error_message = "Invalid username or password"
            return render_template("user.html", m1=error_message)
    else:
        return render_template("user.html")
        



# # -------------------------------Loginact End-----------------------------------------------------------------


   
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
