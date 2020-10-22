#https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/

import os
# Note this Flask instance has not been created globally
# Any configuration, registration and other set up will happen 
# inside the create_app function, then the application is returned. 
# This function is known as the APPLICATION FACTORY

from flask import Flask

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite'),
    )

    # THE TESTS
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in:
        app.config.from_pyfile(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # THE ROUTES
    @app.route('/')
    def hello():
        return "Hello, world"

    # RETURN THE app to start it
    return app