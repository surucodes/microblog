from app import app , db
from app.models import User , Post
import sqlalchemy as sa

app.app_context().push()
#remember class is the relational model and class attributes are the columns. every instance you create of the classes which inherit db.model are going to be new entities/ rows in the database table.
u = User(username = 'john' , email = 'john@example.com ')
db.session.add(u)
db.session.commit()

# Changes to a database are done in the context of a database session, which can be accessed as db.session. Multiple changes can be accumulated in a session and once all the changes have been registered you can issue a single db.session.commit(), which writes all the changes atomically. If at any time while working on a session there is an error, a call to db.session.rollback() will abort the session and remove any changes stored in it. The important thing to remember is that changes are only written to the database when a commit is issued with db.session.commit(). Sessions guarantee that the database will never be left in an inconsistent state.


# Think of author as a bridge: it lets you assign a User object directly to a Post instead of manually assigning the user_id.

# So this:
# p = Post(body='hi', author=u)

# is the same as:
# p = Post(body='hi', user_id=u.id)
# But cleaner, easier, and more object-oriented.

