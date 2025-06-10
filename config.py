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

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    