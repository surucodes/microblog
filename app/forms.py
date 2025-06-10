# The Flask-WTF extension uses Python classes to represent web forms. A form class simply defines the fields of the form as class variables.
from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username' , validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')
# username = StringField('Username')
# 🧠 This adds a text input box for the user to type their username.
# 'Username' is the label that will be shown next to the box.
# Internally, Flask-WTF takes care of naming it username, validating it, and showing it on the HTML page when you write {{ form.username() }}.