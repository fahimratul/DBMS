import functools
import re
from urllib.robotparser import RequestRate
from flask import(
    Blueprint, render_template, request, flash, redirect, url_for, session, g, jsonify
)
from mysql.connector import IntegrityError

from rapid.auth import login_required
from rapid.db import get_bd

from werkzeug.security import generate_password_hash, check_password_hash
import json
import base64


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/approve_volunteer/<int:volunteer_id>', methods=['POST'])
def approve_volunteer(volunteer_id):
    db = get_bd()
    cursor = db.cursor()
    try:
        # Example: Set status to 'approved' for the volunteer
        cursor.execute(
            "UPDATE volunteer SET status = %s WHERE volunteer_id = %s",
            ('free', volunteer_id)
        )
        db.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@bp.route('/decline_volunteer/<int:volunteer_id>', methods=['POST'])
def decline_volunteer(volunteer_id):
    db = get_bd()
    cursor = db.cursor()
    try:
        cursor.execute(
            "DELETE FROM volunteer WHERE volunteer_id = %s",
            (volunteer_id,)
        )
        db.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@bp.route('/unblock_volunteer/<int:volunteer_id>', methods=['POST'])
def unblock_volunteer(volunteer_id):
    db = get_bd()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE volunteer SET status = %s WHERE volunteer_id = %s",
            ('free', volunteer_id)
        )
        db.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/volunteer/<int:volunteer_id>', methods=['GET'])
def get_volunteer(volunteer_id):
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM volunteer WHERE volunteer_id = %s",
        (volunteer_id,)
    )
    volunteer = cursor.fetchone()
    
    if volunteer and volunteer.get('nid_birthcert'):
        image_blob = volunteer['nid_birthcert']
        # Try to detect image type (basic check for PNG/JPEG headers)
        if image_blob.startswith(b'\x89PNG\r\n\x1a\n'):
            mime_type = 'image/png'
        elif image_blob.startswith(b'\xff\xd8'):
            mime_type = 'image/jpeg'
        else:
            mime_type = 'application/octet-stream'
        volunteer['nid'] = f"data:{mime_type};base64,{base64.b64encode(image_blob).decode('utf-8')}"
        print(volunteer['nid'][:30])
    else:
        volunteer['nid'] = None

    if volunteer and volunteer.get('profile_picture'):
        image_blob = volunteer['profile_picture']
        # Try to detect image type (basic check for PNG/JPEG headers)
        if image_blob.startswith(b'\x89PNG\r\n\x1a\n'):
            mime_type = 'image/png'
        elif image_blob.startswith(b'\xff\xd8'):
            mime_type = 'image/jpeg'
        else:
            mime_type = 'application/octet-stream'
        volunteer['profile_picture'] = f"data:{mime_type};base64,{base64.b64encode(image_blob).decode('utf-8')}"
        print(volunteer['profile_picture'][:30])
    else:
        volunteer['profile_picture'] = None

    cursor.execute(
        "SELECT volunteer_id, COUNT(*) AS event_count FROM event WHERE volunteer_id = %s GROUP BY volunteer_id;",
        (volunteer_id,)
    )
    event_count_result = cursor.fetchone()
    volunteer['event_count'] = event_count_result['event_count'] if event_count_result else 0
    
    cursor.execute(
        "SELECT volunteer_id, COUNT(*) AS feedback_count FROM feedback WHERE volunteer_id = %s GROUP BY volunteer_id;",
        (volunteer_id,)
    )
    feedback_count_result = cursor.fetchone()
    volunteer['feedback_count'] = feedback_count_result['feedback_count'] if feedback_count_result else 0

    cursor.close()
    if volunteer:
        return  render_template('admin/volunteer_detail.html', volunteer=volunteer)
    else:
        return jsonify({'success': False, 'error': 'Volunteer not found'}), 404

@bp.route('/block_volunteer/<int:volunteer_id>', methods=['POST'])
def block_volunteer(volunteer_id):
    db = get_bd()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE volunteer SET status = %s WHERE volunteer_id = %s",
            ('block', volunteer_id)
        )
        db.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

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
    cursor.execute('SELECT volunteer_id, name, phone, email, dob, address, pref_address , join_time FROM volunteer where status="free";')
    freevolunteers = cursor.fetchall()
    cursor.execute('SELECT volunteer_id, name, phone, email, dob, address, pref_address , join_time FROM volunteer where status="assign";')
    assignvolunteers = cursor.fetchall()
    cursor.execute('SELECT volunteer_id, name, phone, email, dob, address, pref_address , join_time FROM volunteer where status ="block";')
    blockvolunteers = cursor.fetchall()
    cursor.execute('SELECT volunteer_id, name, phone, email, dob, address, pref_address , join_time FROM volunteer where status="new";')
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
