import email
import functools
import re
from urllib.robotparser import RequestRate
from flask import(
    Blueprint, get_flashed_messages, render_template, request, flash, redirect, url_for, session, g
)
from mysql.connector import IntegrityError
from rapid.db import get_bd

from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """Load user information from session before each request."""
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    
    if user_id is None or user_role is None:
        g.user = None
    else:
        if user_role == 'admin':
            g.user = {
                'id': 0,
                'role': 'admin'
            }
        else:
            db = get_bd()
            cursor = db.cursor()
            
            if user_role == 'donor':
                cursor.execute('SELECT donor_id FROM donor WHERE donor_id = %s', (user_id,))
            elif user_role == 'recipient':
                cursor.execute('SELECT receiver_id FROM receiver WHERE receiver_id = %s', (user_id,))
            elif user_role == 'volunteer':
                cursor.execute('SELECT volunteer_id FROM volunteer WHERE volunteer_id = %s', (user_id,))
            else:
                g.user = None
                return
                
            user_data = cursor.fetchone()
            if user_data:
                g.user = {
                    'id': user_id,
                    'role': user_role
                }
            else:
                g.user = None

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
            if role == 'donor':
                name = request.form.get('name', '')
                phone = request.form.get('phone', '')
                account_name = request.form.get('account_name', '')
                account_id = request.form.get('account_id', '')
                address = request.form.get('address', '')

                cursor.execute('INSERT INTO donor (name, phone, user_name, password, account_name, account_id, address) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                              (name, phone, username, generate_password_hash(password), account_name, account_id, address))
            elif role == 'recipient':
                name = request.form.get('name', '')
                phone = request.form.get('phone', '')
                emergency_phone = request.form.get('emergency_phone', '')
                address = request.form.get('address', '')

                cursor.execute('INSERT INTO receiver (name, phone, user_name, password, emergency_phone, address) VALUES (%s, %s, %s, %s, %s, %s)', 
                              (name, phone, username, generate_password_hash(password), emergency_phone, address))
            elif role == 'volunteer':
                from datetime import date
                name = request.form.get('name', '')
                phone = request.form.get('phone', '')
                email = request.form.get('email', '')
                dob = request.form.get('dob', '')
                address = request.form.get('address', '')
                pref_address = request.form.get('address_2', '')
                profile_file = request.files.get('profile_img')
                profile_picture = profile_file.read() if profile_file else None  # <-- read as bytes
                nid_file = request.files.get('nid_img')  # <-- get file from request.files
                nid_birthcert = nid_file.read() if nid_file else None  # <-- read as bytes
                join_time = date.today()

                cursor.execute(
                    'INSERT INTO volunteer (name, phone, email, dob, address, pref_address, join_time, user_name, password, profile_picture, nid_birthcert) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (name, phone, email, dob, address, pref_address, join_time, username, generate_password_hash(password), profile_picture, nid_birthcert)
                )
            
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
            return render_template('auth/signup_successful.html')
        else:
            errors = get_flashed_messages()
            error = None
            for error in errors:
                break
            return render_template('auth/volunteer_signup.html', error=error)
    return render_template('auth/volunteer_signup.html', error=None)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        role = request.form['role'].lower()
        db = get_bd()
        cursor = db.cursor(dictionary=True)  # This returns dictionaries instead of tuples
        error = None

        if role == 'donor':
            cursor.execute(
                'SELECT donor_id as id, user_name as username, password FROM donor WHERE user_name = %s', 
                (username,)
            )
            user = cursor.fetchone()
        elif role == 'recipient':
            cursor.execute(
                'SELECT receiver_id as id, user_name as username, password FROM receiver WHERE user_name = %s', 
                (username,)
            )
            user = cursor.fetchone()
        elif role == 'volunteer':
            cursor.execute(
                'SELECT volunteer_id as id, user_name as username, password FROM volunteer WHERE user_name = %s', 
                (username,)
            )
            user = cursor.fetchone()
        elif role == 'admin':
            # Generated hash for password 'Admin@12345'
            admin_password_hash = 'scrypt:32768:8:1$8TOWHYfPuOsTCtyR$076b7e2c1d79d9883e5533d282e880797a7ae1b3dfdc3326e466e205ddd835392cf67046492602154c2bc9822e7fe6874c6bcbc1f20a83d61b0e2e45577034db'
            if username == 'admin':
                user = {
                    'id': 0, 
                    'username': 'admin', 
                    'password': admin_password_hash
                }
            else:
                user = None
        else:
            user = None
        
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
                session['user_role'] = role  # Store role in session
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

@bp.route('/success')
def signup_success():
    return render_template('auth/signup_successful.html')
