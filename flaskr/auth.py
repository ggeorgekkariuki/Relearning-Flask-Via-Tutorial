import functools

from flask import (Blueprint, render_template, request, url_for, g, flash, redirect, session)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

"""
A Blueprint is a way to organize a group of related views and other code. 
Rather than registering views and other code directly with an application, 
they are registered with a blueprint. 
Then the blueprint is registered with the application when it is available 
in the factory function.
"""

# The Authentication Blueprint
bp = Blueprint('auth', __name__,url_prefix='/auth')

# If the user id was saved in a session, load the user's information and make 
# the the information available to other views
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

"""
When the user visits the /auth/register URL, the register view will return
 HTML with a form for them to fill out. When they submit the form, it will
 validate their input and either show the form again with an error message 
 or create the new user and go to the login page.
"""
# VIEW: REGISTER
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error=None

        ## Form Validation
        if not username:
            error = "Username is required!" # Ensure field is not empty
        elif not password:
            error = "Password is required!" # Ensure field is not empty
        elif db.execute(
            'SELECT id FROM user WHERE username=?', (username,)
            ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username) 
            # Ensures the user is not already registered

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
            ) # Insert the new user to the DB and encrypt the password
            db.commit() # Save changes to the DB
            return redirect(url_for('auth.login'))
        
        flash(error) #  flash() stores messages that can be retrieved when rendering the template.

    return render_template('auth/register.html') # This HTML will show when initially loading the page or when there is an error


# VIEW: LOGIN
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE username =?', (username,)).fetchone()

        if user is None:
            error = "Incorrect username!"
        elif not check_password_hash(user['password'], password):
            error = "Invalid password!"
            #check_password_hash() hashes the submitted password in the same way as the stored hash and securely compares them. If they match, the password is valid.

        """
        Session is a dict that stores data across requests.
        The data is saved in a 'cookie' that is sent to the browser.
        The browser sends it back with subsequent requests. 
        Flask securely signs the data so that it can't be tampered with.
        """

        if error is None:
            session.clear() 
            session['user_id'] = user['id'] # Save the user's id to the session. Availabl to other views
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# LOGOUT THE USER
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))