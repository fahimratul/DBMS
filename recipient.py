import functools
import re
from flask import(
    Blueprint, render_template, request, flash, redirect, url_for, session, g
)
from mysql.connector import IntegrityError

from flaskr.auth import login_required
from flaskr.db import get_bd

from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('recipient', __name__, url_prefix='/recipient')

@bp.route('/recipient_dashboard')
@login_required
def recipient_dashboard():
    return render_template('recipient/recipient_dashboard.html')
