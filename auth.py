from flask import Blueprint, render_template, request,redirect, url_for 
from models import User
from aidenflask import db
from werkzeug.security import generate_password_hash, check_password_hash
auth_bp=Blueprint('auth',__name__,template_folder='templates')


@auth_bp.route('/login', methods=["GET","POST"])
def login():
    username=request.form.get("username")
    password=request.form.get("password")
    return render_template('login.html' )

@auth_bp.route('/signup', methods=["GET","POST"])
def signup():

    if request.method=="POST":
     data=request.form
     new_user=User(username=data.get("username"),password=generate_password_hash(data.get("password"),method="pbkdf2:sha256"))
     db.session.add(new_user)
     db.session.commit()
     return redirect(url_for("auth.login"))
    return render_template('signup.html' )

 
    
    

