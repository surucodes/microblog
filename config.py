# Flask (or any serious app) needs to know things like:
# Where should I save uploaded files?
# How do I secure the user login form?
# should I show detailed errors (for developers) or hide them (for users)?
# What is the database location?
# Should email alerts be sent from this app?
# How much data can a user upload?
# Which APIs should I use?
# These are not hardcoded inside your logic. Instead, we store them as config settings so we can:
# ✅ Change them easily
# ✅ Keep them separate from the app logic
# ✅ Make them safer (e.g. hide secrets like passwords)
# ✅ Use different settings for development vs production

import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or  'sqlite:///' + os.path.join(basedir,'app.db')
    # A URI (Uniform Resource Identifier) is like the address of your database. It tells Flask-SQLAlchemy where to find your database and how to connect to it.

    # The Flask-SQLAlchemy extension takes the location of the application's database from the SQLALCHEMY_DATABASE_URI configuration variable. As you recall from Chapter 3, it is in general a good practice to set configuration from environment variables, and provide a fallback value when the environment does not define the variable. In this case I'm taking the database URL from the DATABASE_URL environment variable, and if that isn't defined, I'm configuring a database named app.db located in the main directory of the application, which is stored in the basedir variable.