import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


# THE FIRST THING to do when working with SQLite databases and most others
#  is to CREATE A CONNECTION to it.
# Queries and operations are performed using the connection, and then
#  closed after the work is done.
# In web apps the connnection is created when handling the request
#  and closed before the response is sent.

"""
1. g 
    Used to store data that might be accessed by multiple functions during
    a request.
    The connection is stored and reused instead of creating a new one when
    get_db is called a second time
2. current_app
    This points to tyhe Flask Application handling the request.
    An application factory was used; therefore there is no application 
    object yet.
    get_db will be called when the application is created and is handling
    a request -> then current_app can be used
3. sqlite3.connect()
    This establishes a connnection to the file pointed at by the DATABASE 
    configuration key
4. sqlite3.Row
    This tells the connection to return rows that behave like dicts. 
    This allows accessing the columns by name.
5. click
    Used to create beautiful command line interfaces in a composable way
"""

# CONNNECT TO THE DATABASE

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Add the Python functions that will run the SQL commands in 'schema.sql'
"""
1. open_resource
    Opens a file relative to the flaskr package. get_db returns a database 
    connection which is used to execute the commands read from the file.
2. click.command()
    Defines a command line called init-db that calls init_db function and 
    shows a success message to the user
"""
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialised the database')

# REGISTER WITH THE APPLICATION
"""
The close_db and init_db_command functions need to be registered with the 
application instance; otherwise, they won’t be used by the application.
Write a function that takes an application and does the registration.

1. app.teardown_appcontext
    Tells Flask to use this ftn when cleaning up after returning the response
2. app.cli.add_command 
    Adds a new command that can be called with the flask command
"""
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)