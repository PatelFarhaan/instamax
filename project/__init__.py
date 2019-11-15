import os
from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy_utils import create_database, database_exists


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
#  'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Farees143k@localhost/instamax'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('GMAIL_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
mail = Mail(app)
serial = URLSafeTimedSerializer('MYSUPERSECRETKEY')

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_view = 'admin.login'

#########   ###########################################################################################

from project.core.views import core_blueprint
from project.users.views import users_blueprint
from project.admin.views import admins_blueprint
from project.error_pages.handler import error_pages
# from project.utilities.common_utils import get_logger


app.register_blueprint(error_pages)
app.register_blueprint(core_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(admins_blueprint)
import logging


def get_logger(log_file_path=None, name=__name__):
    log_formatter = logging.Formatter("[%(levelname)s] %(asctime)s %(message)s")
    root_logger = logging.getLogger(name)
    root_logger.setLevel(logging.DEBUG)

    if log_file_path:
        log_file_path = log_file_path.rstrip(".log")
        file_handler = logging.FileHandler("{}.log".format(log_file_path))
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    return root_logger

LOGGER_DEBUG = get_logger()  # todo Add log directory path
LOGGER_DEBUG.info("initi")
