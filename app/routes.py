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

@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me = {}'.format(
            form.username.data , form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html',title ='Sign In', form = form)
    



