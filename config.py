# Flask (or any serious app) needs to know things like:
# Where should I save uploaded files?
# How do I secure the user login form?
# should I show detailed errors (for developers) or hide them (for users)?
# What is the database location?
# Should email alerts be sent from this app?
# How much data can a user upload?
# Which APIs should I use?
# These are not hardcoded inside your logic. Instead, we store them as config settings so we can:
# ✅ Change them easily
# ✅ Keep them separate from the app logic
# ✅ Make them safer (e.g. hide secrets like passwords)
# ✅ Use different settings for development vs production

import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or  'sqlite:///' + os.path.join(basedir,'app.db')
    # A URI (Uniform Resource Identifier) is like the address of your database. It tells Flask-SQLAlchemy where to find your database and how to connect to it.

    # The Flask-SQLAlchemy extension takes the location of the application's database from the SQLALCHEMY_DATABASE_URI configuration variable. As you recall from Chapter 3, it is in general a good practice to set configuration from environment variables, and provide a fallback value when the environment does not define the variable. In this case I'm taking the database URL from the DATABASE_URL environment variable, and if that isn't defined, I'm configuring a database named app.db located in the main directory of the application, which is stored in the basedir variable.
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['suraj2005jan@gmail.com']
# 1. MAIL_SERVER = os.environ.get('MAIL_SERVER')
# What is MAIL_SERVER?
# The email server is like the “post office” your app uses to send emails. It’s a service (like Gmail, Outlook, or SendGrid) that handles sending emails over the internet.
# The MAIL_SERVER variable stores the address of this service, like smtp.gmail.com for Gmail. SMTP stands for Simple Mail Transfer Protocol, which is the standard way computers send emails.
# What does os.environ.get('MAIL_SERVER') do?
# This pulls the email server address from an environment variable (like you learned in Chapter 3 for DATABASE_URL). Environment variables are settings stored outside your code (e.g., in a .env file) for security and flexibility.
# If MAIL_SERVER isn’t set (e.g., no .env file), it’s None, which disables email sending.
# Why use it?
# Tells your app which service to use for sending emails. Without it, the app wouldn’t know where to send the error alerts.
# MAIL_SERVER=smtp.gmail.com
# This tells your app to use Gmail’s email server to send error notifications.
# 2. MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
# What is MAIL_PORT?
# A port is like a specific “window” at the post office where your app sends its letters (emails). Each email server has specific ports for sending emails.
# Common ports are:
# 25: A standard port for SMTP, often used for unencrypted emails (less common today).
# 587: Used for secure emails with TLS (most common for Gmail, Outlook, etc.).
# 465: Used for secure emails with SSL (another encryption method).
# What does the code do?
# os.environ.get('MAIL_PORT') gets the port number from an environment variable.
# or 25 means if MAIL_PORT isn’t set, it defaults to port 25.
# int() converts the value (a string, like "587") to a number (587).
# Why use it?
# The port ensures your app connects to the right “window” on the email server. Using the wrong port (e.g., 25 instead of 587 for Gmail) causes failures.
# Example:
# For Gmail, set in .env:
# MAIL_PORT=587
# This tells your app to use Gmail’s secure port for sending emails.
# 3. MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
# What is MAIL_USE_TLS?
# TLS (Transport Layer Security) is like putting your letter in a locked, tamper-proof envelope before sending it. It encrypts the connection between your app and the email server to keep data (like your password) secure.
# MAIL_USE_TLS is a setting that says whether to use this secure “envelope” (True) or not (False).
# What does the code do?
# os.environ.get('MAIL_USE_TLS') checks if the MAIL_USE_TLS environment variable is set.
# is not None means: if MAIL_USE_TLS is set to any value (e.g., true, 1, or even hello), it evaluates to True. If unset, it’s False.
# Why use it?
# Many email servers (like Gmail) require TLS for security. Without it, your app might fail to send emails or expose sensitive data.
# Example:
# In .env, set:
# MAIL_USE_TLS=true
# This enables TLS for Gmail, ensuring secure email sending.
# 4. MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# What is MAIL_USERNAME?
# This is the username for your account on the email server, like your Gmail email address (e.g., suraj@gmail.com).
# Some email servers don’t require a username, but most (like Gmail) do for authentication.
# What does the code do?
# Gets the username from the MAIL_USERNAME environment variable. If unset, it’s None (no username).
# Why use it?
# Authenticates your app to the email server, proving it’s allowed to send emails from your account.
# Example:
# In .env:
# MAIL_USERNAME=suraj@gmail.com
# This tells the server you’re sending emails as suraj@gmail.com.
# 5. MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# What is MAIL_PASSWORD?
# This is the password for your email server account. For Gmail, it’s not your regular password but an App Password (a special code generated in your Google Account settings if 2-factor authentication is enabled).
# What does the code do?
# Gets the password from the MAIL_PASSWORD environment variable. If unset, it’s None (no password).
# Why use it?
# Authenticates your app alongside MAIL_USERNAME. Without it, the email server rejects your app’s attempt to send emails.
# Example:
# In .env:
# MAIL_PASSWORD=abcd-efgh-ijkl-mnop
# This is a 16-character App Password from Google for secure access.
# 6. ADMINS = ['your-email@example.com']
# What is ADMINS?
# A list of email addresses that will receive the error notifications. This is where the app sends alerts when something goes wrong (e.g., a 500 error).
# What does the code do?
# Hardcodes a list with one email (replace your-email@example.com with your actual email, e.g., suraj@example.com).
# Later, you can add more emails if multiple people need alerts (e.g., ['suraj@example.com', 'admin2@example.com']).
# Why use it?
# Specifies who gets notified about errors. Without this, the app wouldn’t know where to send the error emails.
# Example:
# Update to:
# ADMINS = ['suraj@example.com']
# When a 500 error occurs, you’ll get an email at suraj@example.com with the error details.