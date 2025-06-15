# The Flask-WTF extension uses Python classes to represent web forms. A form class simply defines the fields of the form as class variables.
from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import ValidationError,DataRequired,Email,EqualTo
import sqlalchemy as sa 
from app import db
from app.models import User
class LoginForm(FlaskForm):
    username = StringField('Username' , validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')
# username = StringField('Username')
# 🧠 This adds a text input box for the user to type their username.
# 'Username' is the label that will be shown next to the box.
# Internally, Flask-WTF takes care of naming it username, validating it, and showing it on the HTML page when you write {{ form.username() }}.

class RegistrationForm(FlaskForm):
    username = StringField('Username' , validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Pasword' , validators = [DataRequired() , EqualTo('password')])
    submit  = SubmitField('Register')

    def validate_username(self,username) : 
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None : 
            raise ValidationError('Please use a different username.')
        
    def validate_email(self,email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please enter a differnt email address.')
    # When you add any methods that match the pattern validate_<field_name>, WTForms takes those as custom validators and invokes them in addition to the stock validators. I have added two of those methods to this class for the username and email fields.