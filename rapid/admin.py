import functools
import re
from urllib.robotparser import RequestRate
from flask import(
    Blueprint, render_template, request, flash, redirect, url_for, session, g, Response
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
    volunteer_data = cursor.fetchone() #dictionary {'cnt':6}
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
    cursor.execute(
        "SELECT DATE_FORMAT(date, '%Y-%m') AS month, COUNT(*) AS donation_count "
        "FROM donation "
        "WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) "
        "GROUP BY month "
        "ORDER BY month ASC;"
    )
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
    # execute once to create the function in the database, 
    # then can be called as needed
    # DELIMITER //
    # CREATE FUNCTION get_available_stock(item_id INT)
    # RETURNS INT
    # DETERMINISTIC
    # BEGIN
    #     DECLARE qty INT;
    #     SELECT COUNT(*) INTO qty
    #     FROM stock_items
    #     WHERE stock_items.item_id = item_id
    #     AND stock_items.expire_date >= CURDATE();
    #     RETURN qty;
    # END //
    # DELIMITER ;
    cursor.execute("""
        SELECT i.name, 
               get_available_quantity(i.item_id) AS available_quantity
        FROM item i
        LIMIT 5;
    """)
    stock_data = cursor.fetchall() #{name:..., available_quantity:...}

    cursor.execute("""
        SELECT receiver.name AS receiver_name, item.name AS item_name
        FROM donation_receiver
        JOIN receiver ON donation_receiver.receiver_id = receiver.receiver_id
        JOIN stock ON donation_receiver.stock_id = stock.stock_id
        JOIN item ON stock.item_id = item.item_id
        WHERE donation_receiver.date = (
            SELECT MAX(donation_receiver2.date)
            FROM donation_receiver donation_receiver2
            WHERE donation_receiver2.receiver_id = donation_receiver.receiver_id
        );
    """)
    request_data = cursor.fetchall() #{receiver_name:..., item_name:...}

    cursor.execute("""
        SELECT volunteer_id, name, profile_picture FROM volunteer;
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
    return render_template('admin/events.html')

@bp.route('/volunteer_list')
@login_required
def volunteer_list():
    return render_template('admin/volunteer_list.html')

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
