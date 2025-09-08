import functools
import re
from urllib.robotparser import RequestRate
from flask import(
    Blueprint, render_template, request, flash, redirect, url_for, session, g
)
from mysql.connector import IntegrityError

from rapid.auth import login_required
from rapid.db import get_bd

from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('donor', __name__, url_prefix='/donor')

@bp.route('/donor_dashboard')
@login_required
def donor_dashboard():
    return render_template('donor/donor.html')

@bp.route('/donor_profile')
@login_required
def donor_profile():
    return render_template('donor/profile.html') 

@bp.route('/donor_donate')
@login_required
def donor_donate():
    return render_template('donor/donate.html')
 
@bp.route('/donor_history')
@login_required
def donor_history():
    return render_template('donor/history.html') 

@bp.route('/feedback')
@login_required
def donor_feedback():
    donor_id = session.get('user_id')
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT name FROM donor WHERE donor_id = %s",
        (donor_id,)
    )
    donor = cursor.fetchone()
    name = donor['name'] if donor else 'Donor'
    cursor.close()
    return render_template('feedback.html', user_type='donor', name=name)
