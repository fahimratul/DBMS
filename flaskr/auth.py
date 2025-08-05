import functools
import re
from flask import(
    Blueprint, render_template, request, flash, redirect, url_for, session, g
)
from mysql.connector import IntegrityError

from flaskr.db import get_bd

from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_bd()
        cursor = db.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            error = 'Username can only contain letters, numbers, and underscores.'
        elif not password:
            error = 'Password is required.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters long.'
        elif not re.search(r'[A-Z]', password):
            error = 'Password must contain at least one uppercase letter.'
        elif not re.search(r'[a-z]', password):
            error = 'Password must contain at least one lowercase letter.'
        elif not re.search(r'[0-9]', password):
            error = 'Password must contain at least one digit.'
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            error = 'Password must contain at least one special character.'
        
        if error is None:
            try:
                cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s)', (username, generate_password_hash(password)))
                db.commit()
            except IntegrityError:
                error = f"User '{username}' already exists."
            else:
                flash(f"User {username} registered successfully!")
                return redirect(url_for('auth.login'))
        flash(error)
    
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        db = get_bd()
        cursor = db.cursor(dictionary=True)  # This returns dictionaries instead of tuples
        error = None

        cursor.execute(
            'SELECT id, username, password FROM user WHERE username = %s', 
            (username,)
        )
        user = cursor.fetchone()
        
        # Debug: print type of user to see if dictionary cursor is working
        print(f"Debug: user type = {type(user)}, user = {user}")

        if user is None:
            error = "Invalid username"
        else:
            # Now user is a dictionary: {'id': 1, 'username': 'john', 'password': 'hashed_password'}
            if not check_password_hash(user['password'], password):  # type: ignore
                error = "Invalid password"
            else:
                # Login successful - store user in session
                session.clear()
                session['user_id'] = user['id']  # type: ignore
                return redirect(url_for('index'))  # Redirect to home page
        
        if error:
            flash(error)
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('index'))

def login_required(view):
    """Decorator to ensure user is logged in before accessing a view."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user in None:
            flash("You must be logged in to access this page.")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view