from flask import Blueprint, render_template, request,redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from aidenflask import db
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp=Blueprint('auth',__name__,template_folder='templates')
@auth_bp.route('/login', methods=["GET","POST"])
def login():
    if request.method=="POST":
       username=request.form.get("username")
       password=request.form.get("password")
       user = User.query.filter_by(username=username).first()

       if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for("notes.notes"))
       else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@auth_bp.route('/signup', methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        confirm_password=request.form.get("confirm_password")
        email=request.form.get("email")

        error=None

        if not username or not password or not confirm_password or not email:
            error="All fields are required"
        elif len(password) < 6:
            error="Password must be at least 6 characters long"
        elif password != confirm_password:
            error="Passwords do not match"
        elif User.query.filter_by(username=username).first():
            error="Username already exists"
        elif User.query.filter_by(email=email).first():
            error="Email already exists"

        if error:
            return render_template('signup.html', error=error)

        new_user=User(username=username, password=generate_password_hash(password, method="pbkdf2:sha256"), email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template('signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


    
    

