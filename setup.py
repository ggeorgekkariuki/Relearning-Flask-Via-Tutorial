"""
https://flask.palletsprojects.com/en/1.1.x/tutorial/install/
Making the project installable means that you can build a distribution file
 and install that in another environment, just like you installed Flask in
 your project’s environment. This makes deploying your project the same as
 installing any other library, so you’re using all the standard Python 
 tools to manage everything.
"""

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

"""
1. packages
    Tells Python what package directories, and the Python files they contain
     to include.
2. find_packages
    Finds the directories authomatically, no need to type
3. include package data
    This is set to include OTHER files like static and template directiories
4. Manifest.in
    Python needs to this file to tell what this other data is.


# Install the project

pip install -e .

This tells pip to find setup.py in the current directory and install it 
 in development mode.
 This means to make changes to your local code, you'll need to re-install
 if you change the metadata about the project, eg dependencies.
"""