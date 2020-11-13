from flask import (Blueprint, url_for, redirect, render_template, flash, g, request)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# THE BLOG BLUEPRINT
bp = Blueprint('blog', __name__)

# THE ROUTES 

## INDEX PAGE
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        'FROM post p  JOIN user u ON p.author_id = u.id'
        'ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)

## CREATE ROUTE
@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post(title, body, author_id)'
                'VALUES (?,?,?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

"""
The update and delete views will need to fetch a post by id and check if 
the author matches the logged in user.
Avoid duplicity by making a function that will be used in both views.
"""

# FETCH A POST
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} does not exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

## UPDATE ROUTE
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post set title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index')) 
    
    return render_template('blog/update.html', post=post)

## DELETE ROUTE
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id =?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))