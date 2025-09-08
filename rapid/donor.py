import re
from flask import (
    Blueprint, render_template, request, flash, redirect,
    url_for, g, Response, jsonify
)
from datetime import date
from rapid.auth import login_required
from rapid.db import get_bd

bp = Blueprint('donor', __name__, url_prefix='/donor')

# ===================================================
# Icon Map for Items
# ===================================================
ICON_MAP = {
    "Rice": "utensils",
    "Food": "utensils",
    "Food Supplies": "utensils",
    "Blanket": "bed",
    "Clothes": "shirt",
    "Winter Clothing": "shirt",
    "Paracetamol": "capsule",
    "Medicine": "stethoscope",
    "Medical Supplies": "stethoscope",
    "Bottled Water": "droplet",
    "Water Bottle": "droplet",
    "Tent": "house",
    "Hand Sanitizer": "spray-can",
    "Hammer": "hammer",
    "Diesel": "fuel",
    "Money Donation": "currency-dollar",
    "Emergency Radio": "radio",
    "First Aid Kit": "first-aid",
}

# ===================================================
# Utility Functions
# ===================================================
def get_donor_profile(donor_id):
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT d.name, d.phone, d.user_name, d.email, d.account_name, 
                   d.account_id,  -- added this line
                   d.address, d.profile_picture, a.account_name as account_display_name,
                   a.method_name
            FROM donor d
            LEFT JOIN account a ON d.account_id = a.account_id
            WHERE d.donor_id = %s
        """, (donor_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting donor profile: {e}")
        return None
    finally:
        cursor.close()


def get_donor_stats(donor_id):
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT COALESCE(SUM(mt.amount), 0) as total_donated
            FROM money_transfer mt
            JOIN donation d ON mt.donation_id = d.donation_id
            WHERE d.donor_id = %s
        """, (donor_id,))
        total_donated = cursor.fetchone()['total_donated'] or 0

        cursor.execute("SELECT COUNT(*) as donation_count FROM donation WHERE donor_id = %s", (donor_id,))
        donation_count = cursor.fetchone()['donation_count'] or 0

        cursor.execute("SELECT MIN(date) as first_donation FROM donation WHERE donor_id = %s", (donor_id,))
        result = cursor.fetchone()
        first_donation = result['first_donation'] if result else None
        member_since = first_donation.strftime('%b %Y') if first_donation else 'Recently'

        return {'total_donated': float(total_donated), 'donation_count': donation_count, 'member_since': member_since}
    except Exception as e:
        print(f"Error getting donor stats: {e}")
        return {'total_donated': 0, 'donation_count': 0, 'member_since': 'Recently'}
    finally:
        cursor.close()

def get_items_needed():
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT dr.item_id_list, dr.priority_message FROM donation_receiver dr ORDER BY dr.date DESC LIMIT 20")
        requests = cursor.fetchall()
        items_needed = {}
        for req in requests:
            priority = req["priority_message"]
            item_list_str = req["item_id_list"]
            if not item_list_str:
                continue
            for item_str in item_list_str.split("$"):
                if not item_str.strip():
                    continue
                parts = item_str.split("#")
                if len(parts) != 3:
                    continue
                item_id, item_name, qty = parts
                try:
                    qty = int(qty)
                except ValueError:
                    continue
                if item_id not in items_needed:
                    items_needed[item_id] = {"name": item_name, "needed": 0, "urgency": priority, "icon": ICON_MAP.get(item_name, "package")}
                items_needed[item_id]["needed"] += qty
        return list(items_needed.values())
    except Exception as e:
        print(f"Error getting items needed: {e}")
        return []
    finally:
        cursor.close()

def get_donor_history(donor_id):
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT d.donation_id, d.message, d.date, d.item_id_list,
                   mt.amount, a.account_name, a.method_name
            FROM donation d
            LEFT JOIN money_transfer mt ON d.donation_id = mt.donation_id
            LEFT JOIN account a ON mt.account_id = a.account_id
            WHERE d.donor_id = %s
            ORDER BY d.date DESC
        """, (donor_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting donor history: {e}")
        return []
    finally:
        cursor.close()

def get_item_details_by_ids(item_ids_string):
    if not item_ids_string:
        return []
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        item_ids = [int(id.strip()) for id in item_ids_string.split(',') if id.strip().isdigit()]
        if not item_ids:
            return []
        placeholders = ','.join(['%s'] * len(item_ids))
        cursor.execute(f"""
            SELECT i.item_id, i.name, tl.type_name
            FROM item i
            JOIN type_list tl ON i.type_id = tl.type_id
            WHERE i.item_id IN ({placeholders})
        """, item_ids)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting item details: {e}")
        return []
    finally:
        cursor.close()


# ===================================================
# Routes
# ===================================================
@bp.route('/donor_dashboard')
@login_required
def donor_dashboard():
    donor_id = g.user['id']
    stats = get_donor_stats(donor_id)
    items_needed = get_items_needed()
    donor_info = get_donor_profile(donor_id)
    return render_template('donor/donor.html', stats=stats, items_needed=items_needed, donor_info=donor_info)


@bp.route('/donor_profile', methods=['GET', 'POST'])
@login_required
def donor_profile():
    donor_id = g.user['id']
    donor_info = get_donor_profile(donor_id)
    stats = get_donor_stats(donor_id)
    if not donor_info:
        flash('Profile information not found.', 'error')
        return redirect(url_for('donor.donor_dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        account_name = request.form.get('account_name', '').strip()
        address = request.form.get('address', '').strip()
        account_id = request.form.get('account_id', '').strip()

        # Email validation
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('donor.donor_profile'))

        db = get_bd()
        cursor = db.cursor()
        try:
            cursor.execute("""
                UPDATE donor
                SET name=%s, phone=%s, email=%s, account_name=%s, address=%s, account_id=%s
                WHERE donor_id=%s
            """, (name, phone, email, account_name, address, account_id, donor_id))
            db.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('donor.donor_profile'))
        except Exception as e:
            db.rollback()
            print(f"Error updating profile: {e}")
            flash('An error occurred while updating your profile.', 'error')
        finally:
            cursor.close()

    donor_info['profile_picture'] = url_for('donor.get_profile_picture', donor_id=donor_id) if donor_info.get('profile_picture') else 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face'
    return render_template('donor/profile.html', donor_info=donor_info, stats=stats)

@bp.route('/donor_donate')
@login_required
def donor_donate():
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT type_id, type_name FROM type_list")
        item_types = cursor.fetchall()
        cursor.execute("SELECT i.item_id, i.name, tl.type_name FROM item i JOIN type_list tl ON i.type_id = tl.type_id ORDER BY tl.type_name, i.name")
        items = cursor.fetchall()
        return render_template('donor/donate.html', item_types=item_types, items=items)
    except Exception as e:
        print(f"Error getting donation items: {e}")
        flash('Error loading donation form.')
        return redirect(url_for('donor.donor_dashboard'))
    finally:
        cursor.close()


@bp.route('/donor_history')
@login_required
def donor_history():
    donor_id = g.user['id']
    history = get_donor_history(donor_id)
    total_donated = sum(float(d['amount']) for d in history if d.get('amount'))
    donation_count = len(history)
    return render_template('donor/history.html', history=history, total_donated=total_donated, donation_count=donation_count)


@bp.route('/submit_donation', methods=['POST'])
@login_required
def submit_donation():
    donor_id = g.user['id']
    message = request.form.get('message', '')
    item_ids = request.form.getlist('items')
    amount = request.form.get('amount', 0)

    db = get_bd()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO donation (message, date, donor_id, item_id_list) VALUES (%s, %s, %s, %s)", (message, date.today(), donor_id, ','.join(item_ids)))
        donation_id = cursor.lastrowid
        if amount and float(amount) > 0:
            cursor.execute("SELECT account_id FROM donor WHERE donor_id = %s", (donor_id,))
            account_info = cursor.fetchone()
            if account_info:
                cursor.execute("INSERT INTO money_transfer (account_id, donation_id, amount) VALUES (%s, %s, %s)", (account_info[0], donation_id, float(amount)))
        db.commit()
        flash('Donation submitted successfully! Thank you for your generosity.')
    except Exception as e:
        db.rollback()
        print(f"Error submitting donation: {e}")
        flash('Error submitting donation. Please try again.')
    finally:
        cursor.close()
    return redirect(url_for('donor.donor_dashboard'))


@bp.route('/profile_picture/<int:donor_id>')
@login_required
def get_profile_picture(donor_id):
    if donor_id != g.user['id']:
        return redirect(url_for('static', filename='images/default_avatar.png'))
    db = get_bd()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT profile_picture FROM donor WHERE donor_id = %s", (donor_id,))
        result = cursor.fetchone()
        if result and result[0]:
            return Response(result[0], mimetype='image/jpeg')
        return redirect('https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face')
    except Exception as e:
        print(f"Error serving profile picture: {e}")
        return redirect('https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face')
    finally:
        cursor.close()


@bp.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        flash('No file selected.')
        return redirect(url_for('donor.donor_profile'))
    file = request.files['profile_picture']
    if file.filename == '':
        flash('No file selected.')
        return redirect(url_for('donor.donor_profile'))

    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        flash('Only image files are allowed.')
        return redirect(url_for('donor.donor_profile'))

    donor_id = g.user['id']
    db = get_bd()
    cursor = db.cursor()
    try:
        file_data = file.read()
        cursor.execute("UPDATE donor SET profile_picture = %s WHERE donor_id = %s", (file_data, donor_id))
        db.commit()
        flash('Profile picture updated successfully!')
    except Exception as e:
        db.rollback()
        print(f"Error uploading profile picture: {e}")
        flash('Error uploading profile picture. Please try again.')
    finally:
        cursor.close()
    return redirect(url_for('donor.donor_profile'))


@bp.route('/api/donation_details/<int:donation_id>')
@login_required
def get_donation_details(donation_id):
    donor_id = g.user['id']
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT d.donation_id, d.message, d.date, d.item_id_list,
                   mt.amount, a.account_name, a.method_name
            FROM donation d
            LEFT JOIN money_transfer mt ON d.donation_id = mt.donation_id
            LEFT JOIN account a ON mt.account_id = a.account_id
            WHERE d.donation_id = %s AND d.donor_id = %s
        """, (donation_id, donor_id))
        donation = cursor.fetchone()
        if not donation:
            return jsonify({'error': 'Donation not found'}), 404
        items = get_item_details_by_ids(donation.get('item_id_list', ''))
        return jsonify({'donation': donation, 'items': items})
    except Exception as e:
        print(f"Error getting donation details: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        cursor.close()
