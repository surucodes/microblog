#The routes module handle the different URLs that the application supports. 
from app import app 
#this is a view function. 
#A view function is just a Python function that runs when someone visits a specific URL on your Flask website.
from flask import render_template , flash , redirect , url_for
from app.forms import LoginForm

from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request 
from urllib.parse import urlsplit

from app.forms import RegistrationForm
@app.route('/')
@app.route('/index')
@login_required
# When a user that is not logged in accesses a view function protected with the @login_required decorator, the decorator is going to redirect to the login page, but it is going to include some extra information in this redirect so that the application can then return to the original page. If the user navigates to /index, for example, the @login_required decorator will intercept the request and respond with a redirect to /login, but it will add a query string argument to this URL, making the complete redirect URL /login?next=/index. The next query string argument is set to the original URL, so the application can use that to redirect back after login.
# When an unlogged-in user accesses a view protected by the @login_required decorator, it redirects to the login page with extra information to return to the original page. For example, if the user goes to /index, the decorator redirects to /login?next=/index, where ‘next’ is the original URL for post-login redirection.
# Flask-Login uses the @login_required decorator to protect view functions from anonymous users. Placing this decorator below the @app.route decorator in Flask restricts access to authenticated users only.
def index():
    # user = {'username':'Suraj'}
#     return '''
#     <head>
#         <title> Home Page - Microblog </title>
#     </head>
#     <body>
#         <h1> Hello, ''' +user['username']+ '''</h1>

#     </body>
# </html>
# '''
    posts = [
      {
          'author':{'username':'Suraj2'},
          'body': 'Beautiful day in portland!'
      },
      {
          'author':{'username':'Tanishta'},
          'body': 'Beautiful day in portland with my banda!'
      }
  ]
    return render_template("index.html",title='Home Page',posts=posts)
# The render_template() function invokes the Jinja template engine that comes bundled with the Flask framework. Jinja substitutes {{ ... }} blocks with the corresponding values, given by the arguments provided in the render_template() call.

# When a user visits /login, this happens:
# 1.routes.py has a route for /login.
# 2.It creates a LoginForm() from forms.py.
# 3.It passes the form to login.html.
# 4.login.html uses Jinja2 to render the form fields and buttons.
# 5.When user submits, the POST request hits the same route.
# 6.Flask validates the form.
# 7.You redirect or flash messages based on success/failure.
# 8.All data goes into the DB using models.py.

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
#         current_user is a special variable provided by Flask-Login.

# It represents whoever is currently using your website:

# If someone has logged in, current_user is the actual user object from your database.

# If no one is logged in, current_user is an anonymous user (a special object Flask-Login provides)
# current_user = the person using your app right now.

# .is_authenticated = tells you if they’re logged in.

     # checking for the first property of the user login criteria which helps us to find out of a user is logged in or not. this above line handle a case where an already logged-in user mistakenly visits the `/login` page. Using `current_user` from Flask-Login, which represents the current client (either a real user object of the User table or an anonymous one), we check the `is_authenticated` property. If the user is already logged in, we redirect them to the index page.

        return redirect(url_for('index'))
    # `url_for('index')` returns `'/'`, the URL path of the `index` VIEW FUNCTION defined with `@app.route('/')` in your Flask app.

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        # User clicks "Submit" (POST request)
        # Flask-WTF reads the incoming form data from the request.Now form.username.data will contain 'suraj' You can access it in your Flask route to log the user in, etc.
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or password')
            return redirect (url_for('login'))
        login_user(user,remember = form.remember_me.data)
        next_page = request.args.get('next')
        # gets the value of the next argument in the query which is produced by @login_required decorator inorder to redirect to the original page to which the user intended to go in the first place(but login required stopped him so to login first) from the login page Example: if the URL is /login?next=/dashboard, next_page becomes "/dashboard".
        # netloc means "network location" — it includes the domain name and (optional) port.For a URL like https://google.com/page, netloc is google.com.

        if not next_page or urlsplit(next_page).netloc != '':
        # checks for Case 3 mentioned below. Basically, this ensures next_page is a relative URL (like /dashboard), and not an external URL (like http://malliciousevilsite.com).netloc is only present in full URLs (like http://...), so we block those.


            next_page = url_for('index')
        return redirect(next_page) 
        # return redirect(url_for('index'))
        # flash('Login requested for user {}, remember_me = {}'.format(
        #     form.username.data , form.remember_me.data
        # ))
        # return redirect(url_for('index'))

#         Case 1: If the `next` argument is not present in the login URL, the application redirects the user to the default index page. For example, if the login URL is `/login` and there is no `next` argument, the user is redirected to `/`.

#    - Case 2: If the `next` argument is present and points to a relative path, the application redirects the user to that path. For instance, if the login URL is `/login?next=/dashboard`, the user is redirected to `/dashboard`.

#    - Case 3: If the `next` argument is present and points to a full URL with a domain name, the application ignores it for security reasons and redirects the user to the index page. For example, if the login URL is `/login?next=https://malicioussite.com`, the user is redirected to `/` instead of the malicious site.

    return render_template('login.html',title ='Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods= ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # validate_on_submit() is a Flask-WTF method that does two things at once:Checks if the form has been submitted (request.method == "POST")Validates the form data (i.e., runs all the validators on the form fields)
        user = User(username = form.username.data, email= form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations , you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register',form= form)
