import functools
import re
from urllib.robotparser import RequestRate
from flask import(
    Blueprint, render_template, request, flash, redirect, url_for, session, g, jsonify, Response
)
from mysql.connector import IntegrityError

from rapid.auth import login_required
from rapid.db import get_bd
from flask import current_app

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
    volunteer_data = cursor.fetchone() #dictionary {'cnt':10}
    volunteer_cnt = volunteer_data['cnt'] if volunteer_data else 0  # type: ignore[reportGeneralTypeIssues]

    cursor.execute('SELECT COUNT(donor_id) AS cnt FROM donor;')
    donor_data = cursor.fetchone()
    donor_cnt = donor_data['cnt'] if donor_data else 0  # type: ignore[reportGeneralTypeIssues]

    cursor.execute('SELECT COUNT(receiver_id) AS cnt FROM receiver;')
    recipient_data = cursor.fetchone()
    recipient_cnt = recipient_data['cnt'] if recipient_data else 0  # type: ignore[reportGeneralTypeIssues]

    cursor.execute('SELECT SUM(balance) AS available_balance FROM account;')
    account_data = cursor.fetchone()
    available_balance = account_data['available_balance'] if account_data else 0  # type: ignore[reportGeneralTypeIssues]

    # Get donation counts per month for the past year
    cursor.execute("""
        SELECT DATE_FORMAT(date, '%Y-%m') AS month, COUNT(*) AS donation_count
        FROM donation 
        WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY month 
        ORDER BY month ASC;
    """)
    raw_donations = cursor.fetchall()

    # Build a complete list of months (last 12, up to current)
    from datetime import datetime, timedelta
    today = datetime.today()
    months = [(today.replace(day=1) - timedelta(days=30*i)).strftime('%Y-%m') for i in range(12)]
    months = sorted(list(set(months)))  # Ensure chronological order and uniqueness

    # Map SQL results to this list, filling missing months with zero
    donation_map = {row['month']: row['donation_count'] for row in raw_donations}  # type: ignore[reportGeneralTypeIssues]
    donations_by_month = []
    for month in months:
        donations_by_month.append({
            'month': month,
            'donation_count': donation_map.get(month, 0)
        })

    # Sort by month ascending
    donations_by_month.sort(key=lambda x: x['month'])

    cursor.execute("""
        SELECT event_type.event_type,
               event.start_date, 
               event.end_date, 
               event.status 
        FROM event 
        JOIN event_type 
        ON event_type.event_type_id = event.event_type_id
        LIMIT 5;
    """)
    events_data = cursor.fetchall() #{event_type:..., start_date:..., end_date:..., status:...}

    cursor.execute("""
        SELECT d.name,
        COUNT(n.donation_id) AS donation_count
        FROM donor d
        JOIN donation n 
        ON d.donor_id = n.donor_id
        GROUP BY d.donor_id, d.name
        ORDER BY donation_count DESC
        LIMIT 5;
    """)
    top_donors_data = cursor.fetchall() #{name:..., donation_count:...}

    #function to get available stock
    # if the function exists,  no need to create another one
    # Get the database name from the current app configuration
    # cursor.execute("SHOW FUNCTION STATUS WHERE Name = 'get_available_quantity' AND Db = %s", (current_app.config['DATABASE']['database']))
    # function_exists = cursor.fetchone()
    # if not function_exists:
    #     # Create the function if it doesn't exist
    #     cursor.execute("DROP FUNCTION IF EXISTS get_available_quantity")
        
    #     # Change delimiter before creating function
    #     # my sql throws error otherwise
    #     cursor.execute("DELIMITER //")
    #     cursor.execute("""
        #     CREATE FUNCTION get_available_quantity(item_id INT)
        #     RETURNS INT
        #     DETERMINISTIC
        #     READS SQL DATA
        #     BEGIN
        #         DECLARE qty INT;
        #         SELECT IFNULL(SUM(quantity), 0) INTO qty
        #         FROM stock
        #         WHERE stock.item_id = item_id
        #         AND stock.expire_date >= CURDATE();
        #         RETURN qty;
        #     END //
        # """)
    #     # Reset delimiter back to semicolon
    #     cursor.execute("DELIMITER ;")
    
    cursor.execute("""
        SELECT i.name, 
               get_available_quantity(i.item_id) AS available_quantity
        FROM item i
        LIMIT 5;
    """)
    stock_data = cursor.fetchall() #{name:..., available_quantity:...}
    
    # cursor.execute("""
    #     SELECT receiver.name AS receiver_name, item.name AS item_name
    #     FROM donation_receiver
    #     JOIN receiver ON donation_receiver.receiver_id = receiver.receiver_id
    #     JOIN stock ON donation_receiver.stock_id = stock.stock_id
    #     JOIN item ON stock.item_id = item.item_id
    #     WHERE donation_receiver.date = (
    #         SELECT MAX(donation_receiver2.date)
    #         FROM donation_receiver donation_receiver2
    #         WHERE donation_receiver2.receiver_id = donation_receiver.receiver_id
    #     );
    # """)
    cursor.execute("""
        SELECT receiver.name AS receiver_name,
                donation_receiver.item_id_list AS item_ids
                FROM donation_receiver
                JOIN receiver
                ON receiver.receiver_id = donation_receiver.receiver_id
                ORDER BY donation_receiver.date
                LIMIT 5;                
    """) #
    request_raw_data = cursor.fetchall() #[{receiver_name: ..., item_ids: ...}, ...]
    request_data = []
    for row in request_raw_data: #row is a dictionary
        receiver_name = row['receiver_name']
        item_ids_string = row['item_ids']
        
        if item_ids_string:
            items = item_ids_string.split('$')
            temp_dict = {
                'receiver_name': receiver_name,
                'items': [],
                'quantities': []
            }
            for item in items:
                if item.strip():  # Skip empty strings
                    item_info = item.split('#')
                    if len(item_info) >= 3:  # Make sure we have id#name#quantity
                        item_name = item_info[1]
                        item_quantity = item_info[2]
                        temp_dict['items'].append(item_name)
                        temp_dict['quantities'].append(item_quantity)
            request_data.append(temp_dict)

    cursor.execute("""
        SELECT volunteer_id, name, profile_picture FROM volunteer ORDER BY volunteer_id Desc limit 5;
    """)
    raw_volunteer_data = cursor.fetchall()
    
    # Convert binary data to base64 for frontend
    import base64
    volunteer_profile_pics = []
    for volunteer in raw_volunteer_data:
        if volunteer['profile_picture']:  # type: ignore[reportGeneralTypeIssues]
            # Convert binary to base64 string
            base64_image = base64.b64encode(volunteer['profile_picture']).decode('utf-8')  # type: ignore[reportGeneralTypeIssues]
            image_src = f"data:image/jpeg;base64,{base64_image}"
        else:
            # Use None to indicate default image should be used
            image_src = None
        
        volunteer_profile_pics.append({
            'volunteer_id': volunteer['volunteer_id'],  # type: ignore[reportGeneralTypeIssues]
            'name': volunteer['name'],  # type: ignore[reportGeneralTypeIssues]
            'image_src': image_src
        })



    # Prepare data for template
    data = {
        'volunteer_cnt': volunteer_cnt,
        'donor_cnt': donor_cnt,
        'recipient_cnt': recipient_cnt,
        'available_balance': available_balance,
        'donations_by_month': donations_by_month,
        'events': events_data,
        'top_donors': top_donors_data,
        'stock_items': stock_data,
        'requests': request_data,
        'volunteer_profile_pics': volunteer_profile_pics
    }
    # Pass complete monthly data to template
    return render_template('admin/admin_dashboard.html', admin_data=data)  # type: ignore[reportGeneralTypeIssues]

@bp.route('/admin_events')
@login_required
def admin_events():
    db = get_bd()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
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
        LEFT JOIN receiver r ON dr.receiver_id = r.receiver_id
        ORDER BY e.event_id ASC
    """)
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
    return render_template('admin/events.html', events=events)


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
    cursor.execute('SELECT volunteer_id, name, phone, email, dob, address, pref_address , join_time FROM volunteer where status="new" order by join_time desc;')
    newvolunteers = cursor.fetchall()
    cursor.close()
    return render_template('admin/volunteer_list.html', freevolunteers=freevolunteers, assignvolunteers=assignvolunteers, blockvolunteers=blockvolunteers, newvolunteers=newvolunteers)
    

@bp.route('/admin_donors')
@login_required
def admin_donors():
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM donor;')
    donors = cursor.fetchall()
    return render_template('admin/donor_list.html', donors=donors)

@bp.route('/admin_requests')
@login_required
def admin_requests():
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute('''
    SELECT dr.donation_receiver_id,
           dr.receiver_id,
           dr.date,
           dr.priority_message,
           dr.item_id_list,
           dr.additional_item,
           r.name AS receiver_name,
           r.phone,
           r.emergency_phone,
           r.address
           
    FROM donation_receiver dr
    JOIN receiver r ON dr.receiver_id = r.receiver_id
''')

    requests = cursor.fetchall()
    return render_template('admin/requests.html', requests=requests)


@bp.route('/admin_stock')
@login_required
def admin_stock():
    db = get_bd()
    cursor = db.cursor(dictionary=True)

    cursor.execute('''
        SELECT s.stock_id, s.price, s.quantity, s.purchase_date, s.stock_date, s.expire_date,
               s.item_id, i.name AS item_name, s.account_id
        FROM stock s
        LEFT JOIN item i ON s.item_id = i.item_id
    ''')
    stocks = cursor.fetchall()

    return render_template('admin/stock.html', stocks=stocks)


@bp.route('/admin_create_event', methods=['GET', 'POST'])
@login_required
def admin_create_event():
    db = get_bd()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        requester_id = request.form.get('requesterId')  # can be None or ''
        leader_id = request.form.get('teamLeader')           
        event_type_name = request.form.get('eventType')       
        status = 'Pending'  
        location = request.form.get('location')  # can be manual
                                 

    
        cursor.execute("SELECT event_type_id FROM event_type WHERE event_type = %s", (event_type_name,))
        row = cursor.fetchone()
        event_type_id = row['event_type_id'] if row else None

   
        volunteer_ids = request.form.getlist("volunteers")  # ["2","3","5"]
        if leader_id and leader_id not in volunteer_ids:
            volunteer_ids.insert(0, leader_id)
        volunteer_id_list = "$".join(volunteer_ids) + "$" if volunteer_ids else None

    
        item_ids = request.form.getlist('item-id')
        item_names = request.form.getlist('item-name')
        item_quantities = request.form.getlist('item-qty')

        item_string_list = []
        for item_id, item_name, qty in zip(item_ids, item_names, item_quantities):
            if not item_id:  
                item_string_list.append(f"manual#{item_name}#{qty}")
            else:
                cursor.execute("SELECT name FROM item WHERE item_id=%s", (item_id,))
                item_row = cursor.fetchone()
                if item_row:
                    item_name_db = item_row['name']
                    item_string_list.append(f"{item_id}#{item_name_db}#{qty}")

        item_string = "$".join(item_string_list) + "$" if item_string_list else None

        cursor.execute("""
            INSERT INTO event (volunteer_id_list, event_type_id, donation_receiver_id, status, start_date, item_id_list, location)
        VALUES (%s, %s, %s, %s, CURDATE(), %s, %s)
        """, (volunteer_id_list, event_type_id, requester_id if requester_id else None, status, item_string,location))
        
    
        db.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for('admin.admin_create_event'))

    



    cursor.execute("SELECT COUNT(event_id) AS cnt FROM event;")
    result = cursor.fetchone()
    next_event_number = (result['cnt'] if result else 0) + 1  


    cursor.execute("""
    SELECT r.receiver_id, r.name AS receiver_name, r.phone, r.emergency_phone,
           r.address, dr.date AS request_date, dr.priority_message,
           dr.additional_item, dr.item_id_list
    FROM receiver r
    JOIN donation_receiver dr ON r.receiver_id = dr.receiver_id
    WHERE dr.date = (
        SELECT MAX(dr2.date)
        FROM donation_receiver dr2
        WHERE dr2.receiver_id = r.receiver_id
    )
    """)
    rows = cursor.fetchall()

    requesters = {}
    for row in rows:
        receiver_id = row['receiver_id']
        if receiver_id not in requesters:
            requesters[receiver_id] = {
            'id': receiver_id,
            'name': row['receiver_name'],
            "priority": row['priority_message'],
            "additionalItems": row['additional_item'],
            "requestDate": row['request_date'].strftime("%Y-%m-%d"),
            "location": row['address'],
            'contact': row['phone'],
            "emergencyContact": row['emergency_phone'],
            "items": []
        }


        if row['item_id_list']:
            items_raw = row['item_id_list'].split('$')
            for item_str in items_raw:
                if item_str.strip():
                    parts = item_str.split('#')
                    if len(parts) == 3:
                        item_id, item_name, qty = parts
                        requesters[receiver_id]['items'].append({
                            'itemId': int(item_id),
                            'item': item_name,
                            'quantity': int(qty)
                        })

    requesters_list = list(requesters.values())



    cursor.execute("SELECT volunteer_id AS id, name FROM volunteer;")
    volunteers = cursor.fetchall() or []

    cursor.execute("SELECT item_id, name FROM item;")
    all_items = cursor.fetchall()  or []

    cursor.execute("SELECT event_type FROM event_type;")
    event_types = [row['event_type'] for row in cursor.fetchall()] or []

    return render_template(
        "admin/create_event.html",
        event_id=next_event_number,
        requesters=requesters_list,
        volunteers=volunteers,
        event_types=event_types,
        all_items=all_items
    )

