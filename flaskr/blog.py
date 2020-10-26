from flask import (Blueprint, redirect, render_template, g, request, flash, url_for)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# THE POSTS BLUEPRINT
bp = Blueprint('blog', __name__)