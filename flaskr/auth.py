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

