import functools
import re
from flask import(
    Blueprint, render_template, request, flash, redirect, url_for, session, g
)
from mysql.connector import IntegrityError

from flaskr.db import get_bd

from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.auth import login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

@bp.route('/admin_events')
@login_required
def admin_events():
    return render_template('admin/admin_events.html')