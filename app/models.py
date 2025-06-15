from typing import Optional 
# This imports the Optional type hint from Python’s typing module. It’s used to indicate that a variable can either hold a specific type (e.g., str) or be None. In this case, it’s used for the password_hash field, which might be None if a user hasn’t set a password yet (though rare in practice).
import sqlalchemy as sa
# SQLAlchemy is a Python library for working with databases, allowing you to define tables, query data, and manage database connections. Here, it’s used to specify column types (e.g., sa.String).
import sqlalchemy.orm as so 
#Imports SQLAlchemy’s Object-Relational Mapping (ORM) module, aliased as so. The ORM lets you define database tables as Python classes (models) and interact with the database using Python objects instead of raw SQL queries. It’s used here for defining the User model and mapping its attributes to database columns.
from app import db
# Imports the db object from your Flask app’s app/__init__.py. This db is an instance of Flask-SQLAlchemy, a Flask extension that simplifies SQLAlchemy integration with Flask. It’s configured to connect to your database (e.g., SQLite via sqlite:///app.db) and is used to define models and interact with the database.
from datetime import datetime,timezone
from werkzeug.security import generate_password_hash, check_password_hash
#Used to transform a password into a long encoded string through some series of cryptographic operations that have no reverse operation. And two passwords have different cryptographic salts which make them not possible to identify if two people have the same password. 

from flask_login import UserMixin
# instead of Writing All That code for each of the 4 requirement of the flask login, Flask-Login gives you a ready-made class called UserMixin, which already includes all of these, so you don’t have to write them manually. so,UserMixin is a convenient helper class provided by Flask-Login that gives your User model all the basic methods and properties Flask-Login needs.

from app import login 


# This class defines the structure of the user table, including its columns (fields) and their properties. It allows you to create, read, update, and delete (CRUD) user records in the database using Python code.
class User(UserMixin, db.Model):
    # Why is a constructor not needed here ? 
    # When you do this:

    # user = User(username="suraj", email="suraj@example.com")
    # Even though you didn’t write an __init__ method, it still works because:

    # ✅ SQLAlchemy's db.Model base class generates the constructor automatically, using the columns you defined.

    # 🔧 Under the Hood:
    # When you inherit from db.Model, SQLAlchemy:

    # Inspects your class attributes (like username, email, etc.)

    # Generates a constructor that accepts them as keyword arguments

    # Automatically maps those arguments to table columns

    # So this works out of the box:

    #As you are inheriting from the base class db.model,this makes the class User, a database model, meaning it represents a table in your database (named user by default, based on the class name).
    # Each instance of this class will correspond to a row in the user table.
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    # id: so.Mapped[int]: Uses SQLAlchemy’s ORM type hinting to indicate that the id attribute maps to an integer column in the database. The so.Mapped annotation helps tools like linters understand the type of data this column holds.so.Mapped[int] or so.Mapped[str] define the type of the column, and also make values required, or non-nullable in database terms.

    # so.mapped_column(primary_key=True): Defines the id column as the primary key for the user table. A primary key is a unique identifier for each row (user) in the table. By default, SQLAlchemy will auto-increment this value (e.g., 1, 2, 3, ...) for each new user.

    username: so.Mapped[str] = so.mapped_column(sa.String(64), index = True, unique = True)

    # username: so.Mapped[str]: Specifies that the username attribute maps to a string  column in the database.
    # so.mapped_column(sa.String(64), index=True, unique=True):
    # sa.String(64): Defines the column type as a string with a maximum length of 64   characters.
    # index=True: Creates a database index for this column, which speeds up queries (e.g.,searching for a user by username).
    # unique=True: Ensures that each username in the user table is unique, preventing  duplicate usernames.

# Purpose: Stores the user’s username, which must be unique (e.g., no two users can have the username “suraj”). The index improves performance for username-based queries.

    email: so.Mapped[str] = so.mapped_column(sa.String(64), index = True, unique=True)
    password_hash : so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    #  defines that The column can be nullable in database terms.
    posts : so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    def __repr__(self):
        return '<User {}>'.format(self.username)
    # Purpose: Provides a human-readable representation of a User object when printed or inspected, making it easier to debug or test your code.

    def set_password(self,password):
        self.password_hash=generate_password_hash(password, method = 'pbkdf2:sha256')

    def check_password(self,password):
        return check_password_hash(self.password_hash, password )


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index= True, default=lambda : datetime.now(timezone.utc))
    
    # SQLAlchemy's mapped_column (or Column) has a default parameter, which tells it:
    # “If I don’t specify a value for this column when inserting a new row, use this default.”
    # You can give default as return datetime.now(timezone.utc) to return the current time in utc.

    user_id : so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),index=True)
    author: so.Mapped[User] = so.relationship(back_populates = 'posts')

    # author: so.Mapped[User]: Declares a virtual field called author that maps to a User object. This isn’t a column in the post table but a Python-level relationship that SQLAlchemy creates for convenience.
    # so.relationship(back_populates='posts'):
    # so.relationship: Sets up a high level relationship between the Post and User models. It allows you to access the User object associated with a post via post.author (e.g., post.author.username to get the author’s username).
    # back_populates='posts': Specifies that this relationship is bidirectional. The User model must have a corresponding posts field (e.g., posts: so.Mapped[List[Post]] = so.relationship(back_populates='author')) that lets you access all posts by a user via user.posts. This links the two sides of the relationship.
    # Purpose: Simplifies querying related data. Instead of manually querying the User table with user_id, you can directly access the author’s details (e.g., post.author.email).

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
# Preparing the User Model for Flask-Login :

#  But Flask-Login doesn’t know how your User class looks. So it just says:
# “I’ll work with any User model, as long as it gives me 4 basic things.”:

# 1. is_authenticated
# 🔍 What is it?
# Returns True if the user has provided valid credentials (i.e., they’re logged in).

# 2. is_active
# 🔍 What is it?
# Returns True if the user account is active.

# 🔸 Use case: Useful if you want to disable certain user accounts (e.g., banned, deleted).

# 3. is_anonymous
# 🔍 What is it?
# Returns True if the user is not logged in (anonymous).

# 🔸 Use case: Flask-Login uses this to distinguish between a real user and a guest browsing your site.

# 4. get_id()
# 🔍 What is it?
# Returns a unique string ID for the user.

# 🔸 Use case: Flask-Login stores this ID in the session to remember who the user is.

@login.user_loader
# this decorator registers the function as the way to look tp/ a special function that tells Flask-Login how to find a user in your database given their ID.
# User logs in → Flask-Login stores user.id in session.
# New request eg user visits dashboard/→ Flask-Login calls load_user(user_id) internally(the decorator's work').
# Your function retrieves and returns User object.
# Flask-Login sets current_user to that User.
def load_user(id):
# the id is always a string hence convert it into int before returning.
    return db.session.get(User,int(id))
# look inside User table, find the row where id matches primary key id and return the whole User object ex <User id=3, username='suraj', email='suraj@example.com'>
