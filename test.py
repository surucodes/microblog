from app import app, db
from app.models import User, Post
import sqlalchemy as sa
# or Flask and its extensions to have access to the Flask application without having to pass app as an argument into every function, an application context must be created and pushed.
app.app_context().push()
u = User(username='john', email='john@example.com')
db.session.add(u)
db.session.commit()
# Changes to a database are done in the context of a database session, which can be accessed as db.session. Multiple changes can be accumulated in a session and once all the changes have been registered you can issue a single db.session.commit(), which writes all the changes atomically. If at any time while working on a session there is an error, a call to db.session.rollback() will abort the session and remove any changes stored in it. The important thing to remember is that changes are only written to the database when a commit is issued with db.session.commit(). Sessions guarantee that the database will never be left in an inconsistent state.
u = User(username='susan', email='susan@example.com')
db.session.add(u)
db.session.commit()

query = sa.select(User)
users = db.session.scalars(query).all()
users
# The query variable in this example is assigned a basic query that selects all the users. This is achieved by passing the model class to the SQLAlchemy sa.select() query helper function. You will find that most database queries start from a sa.select() call.

# The database session, which above was used to define and commit changes, is also used to execute queries. The db.session.scalars() method executes the database query and returns a results iterator. Calling the all() method of the results object converts the results to a plain list.

# get all posts written by a user
u = db.session.get(User, 1)
u
# <User john>
query = u.posts.select()
posts = db.session.scalars(query).all()
posts
# [<Post my first post!>]

# same, but with a user that has no posts
u = db.session.get(User, 2)
u
# <User susan>
query = u.posts.select()
posts = db.session.scalars(query).all()
posts
# []

# print post author and body for all posts
query = sa.select(Post)
posts = db.session.scalars(query)
for p in posts:
    print(p.id, p.author.username, p.body)

# 1 john my first post!

# get all users in reverse alphabetical order
query = sa.select(User).order_by(User.username.desc())
db.session.scalars(query).all()
# [<User susan>, <User john>]

# get all users that have usernames starting with "s"
query = sa.select(User).where(User.username.like('s%'))
db.session.scalars(query).all()
# [<User susan>]