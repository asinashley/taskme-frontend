from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote_plus

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'taskme**2024'
    root_password = ''
    '''taskme_password = 'taskme**2024'''
    encoded_root_password = quote_plus(root_password)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{encoded_root_password}@localhost/taskme'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        '''since the user_id is just the primary key of our user table, use it in the query for the user'''
        return User.query.get(int(user_id))

    '''blueprint for auth routes in our app'''
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    '''blueprint for non-auth parts of app'''
    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app