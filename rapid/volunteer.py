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


bp = Blueprint('volunteer', __name__, url_prefix='/volunteer')

@bp.route('/volunteer_dashboard')
@login_required
def volunteer_dashboard():
    return render_template('volunteer/volunteer_dashboard.html')

@bp.route('/volunteer_profile')
@login_required
def volunteer_profile():
    return render_template('volunteer/volunteer_profile.html')

@bp.route('/volunteer_task')
@login_required
def volunteer_task():
    return render_template('volunteer/volunteer_task.html')

@bp.route('/volunteer_history')
@login_required
def volunteer_history():
    return render_template('volunteer/volunteer_history.html')
