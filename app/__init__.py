from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
# for implementing features such as allowing access to a page ONLY when logged in, and redirecting to the login in view funtion if not , flask needs to know what is the view function that handles login. The above line is for that purpose. 
db = SQLAlchemy(app)
# This line initializes the Flask-SQLAlchemy extension and connects your Flask app to a database.
migrate = Migrate(app, db)

from app import routes , models
# this is the app variable defined in this script.
# The script above creates the application object as an instance of class Flask imported from the flask package. The __name__ variable passed to the Flask class is a Python predefined variable, which is set to the name of the module in which it is used.
