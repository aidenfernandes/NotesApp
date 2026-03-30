from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db=SQLAlchemy()
DB_NAME="database.db"
from models import User, Note

def create_db(app):
   with app.app_context():
      if not path.exists(DB_NAME):
          db.create_all()


def create():
    app=Flask(__name__)
    app.config["SECRET_KEY"]="aiden"
    app.config["SQLALCHEMY_DATABASE_URI"]=f"sqlite:///{DB_NAME}"
    db.init_app(app)

    login_manager=LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from views import home_bp
    from auth import auth_bp
    from notes import notes_bp
    from models import User, Note

    
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    create_db(app)

    return app