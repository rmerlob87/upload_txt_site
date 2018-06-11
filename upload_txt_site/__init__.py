from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_admin import Admin
from upload_txt_site.config import Config
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


class MyModelView(sqla.ModelView):

    def is_accessible(self):
        try:
            if current_user.username == "admin":
                return current_user.is_authenticated
        except:
            pass

admin = Admin(name='Admin Page for upload_txt_site', template_mode='bootstrap3')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    from upload_txt_site.users.routes import users
    from upload_txt_site.posts.routes import posts
    from upload_txt_site.main.routes import main
    from upload_txt_site.errors.handlers import errors

    from upload_txt_site.models import User, Post
    
    # To create database for first time
    with app.app_context():
        db.create_all()

    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Post, db.session))

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app