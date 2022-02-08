from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message = f'Please login to access this page.'
login_manager.login_message_category = "info"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db'
app.config['SECRET_KEY'] = '1549de229a6c009b2e6ed491'

db = SQLAlchemy(app)

from market_package import routes