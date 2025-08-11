import functools
import re
from urllib.robotparser import RequestRate
from flask import(
    Blueprint, render_template, request, flash, redirect, url_for, session, g
)
from mysql.connector import IntegrityError

from flaskr.db import get_bd

from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """Load user information from session before each request."""
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        db = get_bd()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM user WHERE id = %s', (user_id,)
        )
        g.user = cursor.fetchone()

def registration_handler(role):
    """Handle user registration. Ment to be called from 
    particular register route(e.g., donor_signup,
    recipient_signup, volunteer_signup)"""

    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
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
            cursor.execute('INSERT INTO user (username, password, role) VALUES (%s, %s, %s)', 
                            (username, generate_password_hash(password), role))
            db.commit()
        except IntegrityError:
            error = f"User '{username}' already exists."
        else:
            flash(f"User {username} registered successfully!")
            return redirect(url_for('auth.login'))
    
    if error:
        flash(error)
    return None

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        if 'role' in request.form:
            role = request.form['role']
            if role == 'Donor':
                return redirect(url_for('auth.donor_signup'))
            elif role == 'Recipient':
                return redirect(url_for('auth.recipient_signup'))
            elif role == 'Volunteer':
                return redirect(url_for('auth.volunteer_signup'))
            else:
                flash('Please select a valid role.')
                return redirect(url_for('auth.login'))
        
    #if GET request send back to login page
    return redirect(url_for('auth.login'))



@bp.route('/donor_signup', methods=('GET', 'POST'))
def donor_signup():
    if request.method == 'POST':
        result = registration_handler('donor')
        if result:  # If registration_handler returns a redirect
            return result
    return render_template('auth/donor_signup.html')


@bp.route('/recipient_signup', methods=('GET', 'POST'))
def recipient_signup():
    if request.method == 'POST':
        print("DEBUG: POST request received in recipient_signup")
        print(f"DEBUG: Form data: {dict(request.form)}")
        result = registration_handler('recipient')
        if result:  # If registration_handler returns a redirect
            return result
    return render_template('auth/recipient_signup.html')


@bp.route('/volunteer_signup', methods=('GET', 'POST'))
def volunteer_signup():
    if request.method == 'POST':
        result = registration_handler('volunteer')
        if result:
            return result
    return render_template('auth/volunteer_signup.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        role = request.form['role'].lower()
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
                if role == 'admin':
                    return redirect(url_for('admin.admin_dashboard'))
                elif role == 'donor':
                    return redirect(url_for('donor.donor_dashboard'))
                elif role == 'recipient':
                    return redirect(url_for('recipient.recipient_dashboard'))
                elif role == 'volunteer':
                    return redirect(url_for('volunteer.volunteer_dashboard'))
                else:
                    flash("Invalid role selected.")
                    session.clear()
                    return redirect(url_for('auth.login'))
                
        
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
        if g.user is None:
            flash("You must be logged in to access this page.")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view