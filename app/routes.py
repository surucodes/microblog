#The routes module handle the different URLs that the application supports. 
from app import app 
#this is a view function. 
#A view function is just a Python function that runs when someone visits a specific URL on your Flask website.
from flask import render_template , flash , redirect , url_for
from app.forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Suraj'}
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
    return render_template("index.html",title='m  ', user = user , posts=posts)
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me = {}'.format(
            form.username.data , form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html',title ='Sign In', form = form)
    



