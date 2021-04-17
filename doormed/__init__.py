from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_admin import Admin
import os




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

mail = Mail(app)
admin = Admin(app)

 
login_manager = LoginManager(app)
login_manager.login_view = 'user_login'
login_manager.login_message_category =  'danger'


login_seller = LoginManager(app)
login_seller.login_view = 'seller_login'
login_seller.login_message_category =  'danger'






app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SUBJECT_PREFIX'] = '[QUERY]'
app.config['MAIL_SENDER'] = 'ADMIN <nikitadasmsd@gmail.com>'
app.config['ADMIN'] = os.environ.get('ADMIN')





from doormed.main import routes
from doormed.sellers import routes
from doormed.customers import routes
from doormed.errors import handlers
from doormed.cart import routes



