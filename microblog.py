from app import app
# When I run export FLASK_APP=microblog.py, it means “Hey Flask, my main app is inside the file called microblog.py. So when I say flask run, use that file to start the web app.”
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}