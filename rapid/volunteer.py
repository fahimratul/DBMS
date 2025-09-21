import functools
import re
from urllib.robotparser import RequestRate
from flask import(
    Blueprint, jsonify, render_template, request, flash, redirect, url_for, session, g
)
from mysql.connector import IntegrityError
import base64
from rapid.auth import login_required
from rapid.db import get_bd

from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('volunteer', __name__, url_prefix='/volunteer')

@bp.route('/volunteer_dashboard')
@login_required
def volunteer_dashboard():
    volunteer_id = session.get('user_id')
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT name, profile_picture FROM volunteer WHERE volunteer_id = %s",
        (volunteer_id,)
    )
    volunteer = cursor.fetchone()
    name = volunteer.get('name') if volunteer else 'Volunteer'
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

    # Fetch all event rows and count how many times this volunteer_id appears in volunteer_id_list
    id_start = f"{volunteer_id}$"
    id_end = f"${volunteer_id}$"
    cursor.execute(
        "SELECT COUNT(*) AS event_count FROM event WHERE volunteer_id_list LIKE %s or volunteer_id_list LIKE %s",
        (f"{id_start}%", f"%{id_end}")
    )
    event_count_result = cursor.fetchone()
    cursor.execute(
        "SELECT volunteer_id, COUNT(*) AS feedback_count FROM feedback WHERE volunteer_id = %s GROUP BY volunteer_id;",
        (volunteer_id,)
    )
    feedback_count_result = cursor.fetchone()

    cursor.execute(
        "SELECT event_id,event_type, start_date, item_id_list , status FROM event, event_type WHERE event.event_type_id = event_type.event_type_id AND (volunteer_id_list LIKE %s or volunteer_id_list LIKE %s) AND status != 'completed' ORDER BY start_date DESC",
        (f"{id_start}%", f"%{id_end}%")
    )
    events = cursor.fetchall()
    # Fetch the result to clear the unread result
    cursor.fetchone()
    if not event_count_result:
        event_count_result = {'event_count': 0}
    if not feedback_count_result:
        feedback_count_result = {'feedback_count': 0}
    cursor.close()
    return render_template('volunteer/volunteer_dashboard.html', event_count_result=event_count_result['event_count'], feedback_count_result=feedback_count_result['feedback_count'], volunteer=volunteer, events=events)

@bp.route('/profile')
@login_required
def profile():
    volunteer_id = session.get('user_id')
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

    if volunteer:
        return  render_template('volunteer/profile.html', volunteer=volunteer)
    else:
        return jsonify({'success': False, 'error': 'Volunteer not found'}), 404
    

    

@bp.route('/volunteer_tasks')
@login_required
def volunteer_tasks():
    volunteer_id = session.get('user_id')
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    id_start = f"{volunteer_id}$"
    id_end = f"${volunteer_id}$"
    print(f"{id_start} {id_end}")
    
    cursor.execute("""SELECT 
            e.event_id,
            et.event_type,
            e.status,
            e.start_date,
            e.end_date,
            e.volunteer_id_list,
            e.item_id_list,
            e.donation_receiver_id,
            dr.priority_message,
            dr.additional_item,
            dr.date AS request_date,
            r.name AS requester_name,
            r.phone AS requester_contact,
            r.address AS location
        FROM event e
        LEFT JOIN event_type et ON e.event_type_id = et.event_type_id
        LEFT JOIN donation_receiver dr ON e.donation_receiver_id = dr.donation_receiver_id
        LEFT JOIN receiver r ON dr.receiver_id = r.receiver_id  where (e.volunteer_id_list LIKE %s or e.volunteer_id_list LIKE %s)
        ORDER BY e.event_id ASC
    """, (f"{id_start}%", f"%{id_end}%"))
    events = cursor.fetchall()
    cursor.execute("SELECT volunteer_id, name, phone FROM volunteer")
    volunteers = cursor.fetchall()
    volunteer_dict = {v['volunteer_id']: {'volunteer_id': v['volunteer_id'], 'name': v['name'], 'phone': v['phone']} for v in volunteers}
    for ev in events:
        vol_ids = [vid for vid in ev['volunteer_id_list'].split('$') if vid]  # remove empty strings
        ev['volunteers'] = [
            volunteer_dict.get(int(vid), {'name': 'Unknown', 'phone': 'Unknown', 'volunteer_id': vid})
            for vid in vol_ids
        ]
    cursor.close()
    return render_template('volunteer/volunteer_tasks.html', events=events)


@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    volunteer_id = session.get('user_id')
    data = request.get_json()
    required_fields = ['name', 'phone', 'email', 'account_name', 'address']
    if not all(data.get(field) for field in required_fields):
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, data['email']):
        return jsonify({'success': False, 'message': 'Invalid email address.'}), 400

    db = get_bd()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            UPDATE volunteer
            SET name = %s, phone = %s, email = %s, user_name = %s, address = %s
            WHERE volunteer_id = %s
            """,
            (data['name'], data['phone'], data['email'], data['account_name'], data['address'], volunteer_id)
        )
        db.commit()
        return jsonify({'success': True})  # <-- Add this line
    except IntegrityError:
        db.rollback()
        return jsonify({'success': False, 'message': 'Database error.'}), 500
    finally:
        cursor.close()


@bp.route('/update_profile_picture', methods=['POST'])
@login_required
def update_profile_picture():
    volunteer_id = session.get('user_id')
    # The file input field in your HTML is named "profilePicInput"
    file = request.files.get('profilePicInput')
    if not file or file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('volunteer.profile'))

    image_data = file.read()
    db = get_bd()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE volunteer SET profile_picture = %s WHERE volunteer_id = %s",
            (image_data, volunteer_id)
        )
        db.commit()
        flash('Profile picture updated successfully.', 'success')
    except IntegrityError:
        db.rollback()
        flash('Database error.', 'error')
    finally:
        cursor.close()
    return redirect(url_for('volunteer.profile'))

@bp.route('/feedback')
@login_required
def volunteer_feedback():
    volunteer_id = session.get('user_id')
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT name FROM volunteer WHERE volunteer_id = %s",
        (volunteer_id,)
    )
    volunteer = cursor.fetchone()
    name = volunteer['name'] if volunteer else 'Volunteer'
    cursor.close()
    return render_template('feedback.html', user_type='volunteer', name=name)
