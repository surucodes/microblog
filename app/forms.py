# The Flask-WTF extension uses Python classes to represent web forms. A form class simply defines the fields of the form as class variables.
from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import ValidationError,DataRequired,Email,EqualTo
import sqlalchemy as sa 
from app import db
from app.models import User
from wtforms import TextAreaField
from wtforms.validators import Length

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

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0 , max=140)])
    submit = SubmitField('Submit')
    # *args: Stands for “arguments.” It’s a way to accept any number of positional arguments (like a list of values) passed to the function without needing to name them.Example: If you call EditProfileForm("suraj", 1, 2), *args captures 1, 2
    # **kwargs: Stands for “keyword arguments.” It accepts any number of named arguments (like a dictionary of key-value pairs).Example: If you call EditProfileForm("suraj", data="form_data", debug=True), **kwargs captures data="form_data", debug=True

    def __init__(self, original_username,*args,  **kwargs):
        super().__init__(*args, **kwargs)
        #Calls the parent class’s (FlaskForm) __init__ method, passing along any *args and **kwargs. This ensures the form is properly initialized with Flask-WTF’s default setup (e.g., form data, CSRF protection).Analogy: It’s like saying, “Set up the form the way Flask-WTF expects, then I’ll add my custom stuff.” we basically make another constructor so that we can modify the parent constructor by adding our own stuff.
        self.original_username = original_username
        # store original username in  variable.

    # A custom validation method for the username field. Flask-WTF automatically calls methods named validate_<field_name> (e.g., validate_username) to check if the input is valid. flask wtf checks for custom validators whenever rest of the validators are being checked.
    def validate_username(self,username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a differnt username.')
            # Whenever a validation error is raised by this, the html file edit_profile catches it in the 
            # {% for error in form.about_me.errors %}
            # <span style="color: red;">[{{ error }}]</span>
            # {% endfor %}
            # and then the validation isnt passed and no changes in the database is made.
# if a user tries to save their profile with their current username (unchanged), the app might incorrectly flag it as a duplicate because that username already exists in the database (it’s theirs!). This code fixes that by allowing the original username to pass validation while still checking for duplicates if the username is changed.
# Case 1: Enters “suraj” (same as original_username).username.data != self.original_username is False, so no database check.Validation passes, form submits.
# Case 2: Enters “john” (new username).username.data != self.original_username is True, so checks database.If “john” exists, raises ValidationError (“Please use a different username.”).If “john” is free, validation passes.