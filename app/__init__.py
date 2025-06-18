from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
app = Flask(__name__)

app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
# for implementing features such as allowing access to a page ONLY when logged in, and redirecting to the login in view funtion if not , flask needs to know what is the view function that handles login. The above line is for that purpose. 
db = SQLAlchemy(app)
# This line initializes the Flask-SQLAlchemy extension and connects your Flask app to a database.
migrate = Migrate(app, db)

from app import routes , models, errors
# this is the app variable defined in this script.
# The script above creates the application object as an instance of class Flask imported from the flask package. The __name__ variable passed to the Flask class is a Python predefined variable, which is set to the name of the module in which it is used.

if not app.debug:#check means this logging code only runs in production (when app.debug is False).
    if app.config['MAIL_SERVER']:
        auth=None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure =None
        if app.config['MAIL_USE_TLS']:
            secure=()
        mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
#  But in essence, the code above creates a SMTPHandler instance, sets its level so that it only reports errors and not warnings, informational or debugging messages, and finally attaches it to the app.logger object from Flask.

# In Python’s logging module, a handler is something that decides where the log messages go.
# For example:
# Console output? Use StreamHandler
# File? Use FileHandler
# Rotating file? Use RotatingFileHandler
# Email? Use SMTPHandler

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    # A tool that writes log messages to a file (microblog.log) and "rotates" (i.e when the log file meets the maxbytes storage, it makes another file and the old one is archived and max upto 10 old files are kept and rest are discarded) it when it gets too big,creating backups.After some activity, you’ll see microblog/logs/microblog.log (current logs) and backups like microblog.log.1 if the file exceeds 10KB.
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    # choosnig the format of logs.
    file_handler.setLevel(logging.INFO)
    # The logger decides what messages the app generates, and the handler decides what messages get written to the file. Setting both ensures only INFO and higher-level messages (e.g., WARNING, ERROR) are logged to microblog.log.
    app.logger.addHandler(file_handler)
    # Flask provides a built-in “logger” (like a diary keeper) for your app to record events. app.logger is where you send messages to be logged.
    # Attaches the RotatingFileHandler to app.logger, telling Flask to write log messages to microblog.log (in addition to any other handlers, like the email handler for errors).
    # we create a rotating file source first (logs/microblog.log), specify its format, its level and then add it to the built in flask logger app.logger.
    # Why?:
    # Connects the logging system to the file, so all app.logger messages (e.g., app.logger.info("Message")) go to microblog.log.
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
#    app.logger.setLevel(logging.INFO): Sets the app’s logger to record INFO and higher-level messages, matching the file handler’s level.
#    app.logger.info('Microblog startup'): Writes a message to the log file when the app starts, marking the event. 

# Logger (app.logger): The Flask app’s “diary keeper” that collects all log messages (e.g., “app started” or “user logged in”). It decides which messages are important enough to process based on its level (e.g., INFO).

# Handler (file_handler): A tool that decides where to send log messages (e.g., to microblog.log). It also has a level to filter which messages it writes to the file.













from app import routes, models, errors