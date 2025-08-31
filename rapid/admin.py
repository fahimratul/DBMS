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


bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    db  = get_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(volunteer_id) AS cnt FROM volunteer;')
    volunteer_cnt = cursor.fetchone() # {cnt:6}
    return render_template('admin/admin_dashboard.html', volunteer_cnt=volunteer_cnt['cnt'])  # type: ignore

@bp.route('/admin_events')
@login_required
def admin_events():
    return render_template('admin/events.html')

@bp.route('/volunteer_list')
@login_required
def volunteer_list():
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM volunteer where status="free";')
    freevolunteers = cursor.fetchall()
    cursor.execute('SELECT * FROM volunteer where status="assign";')
    assignvolunteers = cursor.fetchall()
    cursor.execute('SELECT * FROM volunteer where status ="block";')
    blockvolunteers = cursor.fetchall()
    cursor.execute('SELECT * FROM volunteer where status="new";')
    newvolunteers = cursor.fetchall()   
    cursor.close()
    return render_template('admin/volunteer_list.html', freevolunteers=freevolunteers, assignvolunteers=assignvolunteers, blockvolunteers=blockvolunteers, newvolunteers=newvolunteers)
    


@bp.route('/admin_donors')
@login_required
def admin_donors():
    return render_template('admin/donor_list.html')

@bp.route('/admin_requests')
@login_required
def admin_requests():
    return render_template('admin/requests.html')

@bp.route('/admin_stock')
@login_required
def admin_stock():
    return render_template('admin/stock.html')

@bp.route('/admin_create_event', methods=['GET', 'POST'])
@login_required
def admin_create_event():
    return render_template('admin/create_event.html')
