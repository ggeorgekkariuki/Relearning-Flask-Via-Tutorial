"""
https://flask.palletsprojects.com/en/1.1.x/tutorial/tests/

This file will contain setup functions called 'fixtures' that each test uses.
Python modules start with 'test_'

Install pytest and coverage in your environment

The 'app' fixture will call the application factory in __init__.py and 
 pass 'test_config' to configure the application and db for testing.

NB: A fixture is function that needs to run first before each test.
The purpose of fixtures is to provide a fixed baseline upon which tests can reliably and repeatedly execute.
"""

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    
    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

'''
1. tempfile.mkstemp
tempfile.mkstemp creates a temporary file that returns a file object and
 the name of the file at the same time. The DATABASE path is overridden so 
 it points to this temporary path instead of the instance folder. 
 After setting the path, the DATABASE tables are created and the test data
 is inserted (test/data.sql).
 When the test is complete, the temporary file is closed and removed.

2. TESTING
Tells Flask that the app is in test mode

3. Client and Runner Fixtures
Client - These use the created app fixture to make requests to the
 application without running the server
Runner - creates a runner that can call the Click conmmands registered
 with the application. 
'''

# AUTHENTICATION
'''
This class is used to ensure that the 'test' user is logged in to access all
 the views that require authentication before accessing the view.
'''
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password':password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

''' 
With the auth fixture we can call '/auth/login' to log in as test user
'''
@pytest.fixture
def auth(client):
    return AuthActions(client)