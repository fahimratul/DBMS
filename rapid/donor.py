import re
from flask import (
    Blueprint, render_template, request, flash, redirect,
    url_for, g, Response, jsonify, session
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
    """Get donor profile information from database"""
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT d.donor_id, d.name, d.phone, d.user_name, d.email, d.account_name, 
                   d.account_id, d.address, d.profile_picture, a.account_name as account_display_name,
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

def get_donor_name(donor_id):
    """Get just the donor name for display purposes"""
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name FROM donor WHERE donor_id = %s", (donor_id,))
        result = cursor.fetchone()
        return result['name'] if result else 'Donor'
    except Exception as e:
        print(f"Error getting donor name: {e}")
        return 'Donor'
    finally:
        cursor.close()

def get_donor_stats(donor_id):
    """Get donor statistics"""
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
    """Get items that are currently needed"""
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
    """Get donor's donation history"""
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
    """Get item details by comma-separated IDs"""
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

def get_available_accounts():
    """Get all available payment accounts"""
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT account_id, account_name, method_name FROM account ORDER BY method_name, account_name")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting accounts: {e}")
        return []
    finally:
        cursor.close()

# ===================================================
# Routes
# ===================================================
@bp.route('/download_receipt/<int:donation_id>')
@login_required
def download_receipt(donation_id):
    """Generate and download a text receipt for a donation"""
    donor_id = g.user['id']
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT d.donation_id, d.message, d.date, d.item_id_list,
                   mt.amount, a.account_name, a.method_name, dn.name as donor_name
            FROM donation d
            LEFT JOIN money_transfer mt ON d.donation_id = mt.donation_id
            LEFT JOIN account a ON mt.account_id = a.account_id
            LEFT JOIN donor dn ON d.donor_id = dn.donor_id
            WHERE d.donation_id = %s AND d.donor_id = %s
        """, (donation_id, donor_id))
        donation = cursor.fetchone()
        if not donation:
            return Response('Donation not found.', status=404)

        # Format items
        items = donation.get('item_id_list', '')
        if items:
            items_str = items.replace('$', ', ')
        else:
            items_str = 'None'

        # Format receipt text
        receipt = f"""
RAPID Donation Receipt
----------------------
Donation ID: {donation['donation_id']}
Donor Name: {donation.get('donor_name', 'Unknown')}
Date: {donation['date'].strftime('%Y-%m-%d') if donation['date'] else 'Unknown'}
Message: {donation['message'] or 'None'}
Amount: Tk {donation['amount'] if donation['amount'] else 'Items Only'}
Items: {items_str}
Payment Method: {donation['method_name'] or 'N/A'} {f'({donation["account_name"]})' if donation['account_name'] else ''}
Status: Completed
----------------------
Thank you for your generosity!
"""
        return Response(receipt, mimetype='text/plain', headers={
            'Content-Disposition': f'attachment; filename=receipt_{donation_id}.txt'
        })
    except Exception as e:
        print(f"Error generating receipt: {e}")
        return Response('Error generating receipt.', status=500)
    finally:
        cursor.close()

@bp.route('/download_all_receipts')
@login_required
def download_all_receipts():
    """Download all receipts for the current donor as a single text file"""
    donor_id = g.user['id']
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT d.donation_id, d.message, d.date, d.item_id_list,
                   mt.amount, a.account_name, a.method_name, dn.name as donor_name
            FROM donation d
            LEFT JOIN money_transfer mt ON d.donation_id = mt.donation_id
            LEFT JOIN account a ON mt.account_id = a.account_id
            LEFT JOIN donor dn ON d.donor_id = dn.donor_id
            WHERE d.donor_id = %s
            ORDER BY d.date DESC
        """, (donor_id,))
        donations = cursor.fetchall()
        
        if not donations:
            # Return a simple message file if no donations
            all_receipts_text = "No donations found for this donor."
        else:
            all_receipts = []
            for donation in donations:
                # Format items
                items = donation.get('item_id_list', '')
                item_lines = []
                
                if items:
                    for item in items.split('$'):
                        if item.strip():
                            parts = item.split('#')
                            if len(parts) == 3:
                                item_name = parts[1]
                                item_qty = parts[2]
                                item_lines.append(f"- {item_name} x{item_qty}")
                
                items_str = '\n'.join(item_lines) if item_lines else 'None'
                
                receipt = f"""
RAPID Donation Receipt
=======================
Donation ID: {donation['donation_id']}
Donor Name: {donation.get('donor_name', 'Unknown')}
Date: {donation['date'].strftime('%Y-%m-%d') if donation['date'] else 'Unknown'}
Message: {donation['message'] or 'None'}
Amount: Tk {donation['amount'] if donation['amount'] else 'Items Only'}
Items: 
{items_str}
Payment Method: {donation['method_name'] or 'N/A'} {f'({donation["account_name"]})' if donation['account_name'] else ''}
Status: Completed

Thank you for your generosity!
"""
                all_receipts.append(receipt)
            
            # Join all receipts with separator
            all_receipts_text = '\n\n' + '='*50 + '\n\n'.join(all_receipts)
        
        # Create filename with current date
        filename = f'all_receipts_{date.today().strftime("%Y%m%d")}.txt'
        
        # Create response with proper headers - THIS IS KEY!
        response = Response(all_receipts_text)
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-Length'] = str(len(all_receipts_text.encode('utf-8')))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
        
    except Exception as e:
        print(f"Error generating all receipts: {e}")
        # Return error as downloadable file for debugging
        error_text = f"Error generating receipts: {str(e)}"
        response = Response(error_text)
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = 'attachment; filename="error.txt"'
        return response
    finally:
        cursor.close()

@bp.route('/donor_dashboard')
@login_required
def donor_dashboard():
    """Donor dashboard page"""
    donor_id = g.user['id']
    stats = get_donor_stats(donor_id)
    items_needed = get_items_needed()
    donor_info = get_donor_profile(donor_id)
    donor_name = get_donor_name(donor_id)
    return render_template('donor/donor.html', 
                         stats=stats, 
                         items_needed=items_needed, 
                         donor_info=donor_info,
                         donor_name=donor_name)

@bp.route('/donor_profile', methods=['GET', 'POST'])
@login_required
def donor_profile():
    """Donor profile page with edit functionality"""
    donor_id = g.user['id']
    donor_info = get_donor_profile(donor_id)
    stats = get_donor_stats(donor_id)
    donor_name = get_donor_name(donor_id)
    
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
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+
        if email and not re.match(email_regex, email):
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

    # Set default profile picture URL
    if donor_info.get('profile_picture'):
        donor_info['profile_picture_url'] = url_for('donor.get_profile_picture', donor_id=donor_id)
    else:
        donor_info['profile_picture_url'] = url_for('static', filename='images/default_user.png')
    
    # Get available accounts for the dropdown
    available_accounts = get_available_accounts()
    
    return render_template('donor/profile.html', 
                         donor_info=donor_info, 
                         stats=stats,
                         donor_name=donor_name,
                         available_accounts=available_accounts)

@bp.route('/donor_donate')
@login_required
def donor_donate():
    """Donation page"""
    donor_id = g.user['id']
    donor_name = get_donor_name(donor_id)
    
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT type_id, type_name FROM type_list")
        item_types = cursor.fetchall()
        cursor.execute("SELECT i.item_id, i.name, tl.type_name FROM item i JOIN type_list tl ON i.type_id = tl.type_id ORDER BY tl.type_name, i.name")
        items = cursor.fetchall()
        return render_template('donor/donate.html', 
                             item_types=item_types, 
                             items=items,
                             donor_name=donor_name)
    except Exception as e:
        print(f"Error getting donation items: {e}")
        flash('Error loading donation form.', 'error')
        return redirect(url_for('donor.donor_dashboard'))
    finally:
        cursor.close()

@bp.route('/donor_history')
@login_required
def donor_history():
    """Donor donation history page"""
    donor_id = g.user['id']
    history = get_donor_history(donor_id)
    donor_name = get_donor_name(donor_id)
    total_donated = sum(float(d['amount']) for d in history if d.get('amount'))
    donation_count = len(history)
    return render_template('donor/history.html', 
                         history=history, 
                         total_donated=total_donated, 
                         donation_count=donation_count,
                         donor_name=donor_name)

@bp.route('/submit_donation', methods=['POST'])
@login_required
def submit_donation():
    """Submit a new donation - Fixed version for item storage"""
    donor_id = g.user['id']
    message = request.form.get('message', '')
    donation_type = request.form.get('donation_type', '')
    
    db = get_bd()
    cursor = db.cursor()
    
    try:
        if donation_type == 'money':
            # Handle monetary donation
            amount = request.form.get('amount', 0)
            payment_method = request.form.get('payment_method', '')
            
            # Validate amount
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Amount must be positive")
            except (ValueError, TypeError):
                flash('Please enter a valid amount.', 'error')
                return redirect(url_for('donor.donor_donate'))
            
            # Insert into donation table with NULL for item_id_list
            cursor.execute(
                "INSERT INTO donation (message, date, donor_id, item_id_list) VALUES (%s, %s, %s, %s)", 
                (message, date.today(), donor_id, None)
            )
            donation_id = cursor.lastrowid
            
            # Get account_id based on payment method
            cursor.execute(
                "SELECT account_id FROM account WHERE method_name LIKE %s LIMIT 1", 
                (f"%{payment_method}%",)
            )
            account_result = cursor.fetchone()
            account_id = account_result[0] if account_result else 1  # Default to first account if not found
            
            # Insert into money_transfer table
            cursor.execute(
                "INSERT INTO money_transfer (account_id, donation_id, amount) VALUES (%s, %s, %s)", 
                (account_id, donation_id, amount)
            )
            
            flash(f'Thank you for your monetary donation of Tk{amount}!', 'success')
            
        elif donation_type == 'items':
            # Handle item donation
            items = request.form.getlist('items')
            quantities = request.form.getlist('quantity')
            
            # Validate that we have items
            if not items or not any(item for item in items if item):
                flash('Please select at least one item to donate.', 'error')
                return redirect(url_for('donor.donor_donate'))
            
            # Build item_id_list string in the format: item_id#item_name#quantity$...
            item_id_list_parts = []
            
            for i, item_id in enumerate(items):
                if item_id and item_id.strip():  # Only process if item is selected and not empty
                    try:
                        # Validate item_id is numeric
                        item_id_int = int(item_id)
                        
                        # Get quantity (default to 1 if not provided or invalid)
                        try:
                            quantity = int(quantities[i]) if i < len(quantities) and quantities[i] else 1
                            if quantity <= 0:
                                quantity = 1
                        except (ValueError, IndexError):
                            quantity = 1
                        
                        # Get item name and type from database
                        cursor.execute("""
                            SELECT i.name, tl.type_name 
                            FROM item i 
                            JOIN type_list tl ON i.type_id = tl.type_id 
                            WHERE i.item_id = %s
                        """, (item_id_int,))
                        
                        item_info = cursor.fetchone()
                        if item_info:
                            item_name = item_info[0]
                            type_name = item_info[1]
                            # Format: item_id#item_name (type)#quantity
                            item_string = f"{item_id_int}#{item_name} ({type_name})#{quantity}"
                            item_id_list_parts.append(item_string)
                        else:
                            print(f"Warning: Item with ID {item_id_int} not found in database")
                            
                    except ValueError:
                        print(f"Warning: Invalid item_id '{item_id}' - not a number")
                        continue
            
            # Check if we have valid items after processing
            if not item_id_list_parts:
                flash('No valid items were selected. Please try again.', 'error')
                return redirect(url_for('donor.donor_donate'))
            
            # Join all item strings with ' separator
            item_id_list = '.join(item_id_list_parts) + '  # Add trailing $ as per your format
            
            # Insert into donation table with item_id_list
            cursor.execute(
                "INSERT INTO donation (message, date, donor_id, item_id_list) VALUES (%s, %s, %s, %s)", 
                (message, date.today(), donor_id, item_id_list)
            )
            
            item_count = len(item_id_list_parts)
            flash(f'Thank you for donating {item_count} item(s)!', 'success')
        
        else:
            flash('Invalid donation type selected.', 'error')
            return redirect(url_for('donor.donor_donate'))
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(f"Error submitting donation: {e}")
        flash('Error submitting donation. Please try again.', 'error')
    finally:
        cursor.close()
    
    return redirect(url_for('donor.donor_donate'))

@bp.route('/profile_picture/<int:donor_id>')
@login_required
def get_profile_picture(donor_id):
    """Serve donor profile picture"""
    # Security check - only allow users to access their own profile picture
    if donor_id != g.user['id']:
        return redirect('https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face')
    
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
    """Upload new profile picture"""
    if 'profile_picture' not in request.files:
        flash('No file selected.', 'error')
        return redirect(url_for('donor.donor_profile'))
    
    file = request.files['profile_picture']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('donor.donor_profile'))

    # Validate file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        flash('Only image files (PNG, JPG, JPEG, GIF) are allowed.', 'error')
        return redirect(url_for('donor.donor_profile'))

    # Validate file size (max 5MB)
    file.seek(0, 2)  # Seek to end of file
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    if file_size > 5 * 1024 * 1024:  # 5MB limit
        flash('File size must be less than 5MB.', 'error')
        return redirect(url_for('donor.donor_profile'))

    donor_id = g.user['id']
    db = get_bd()
    cursor = db.cursor()
    try:
        file_data = file.read()
        cursor.execute("UPDATE donor SET profile_picture = %s WHERE donor_id = %s", (file_data, donor_id))
        db.commit()
        flash('Profile picture updated successfully!', 'success')
    except Exception as e:
        db.rollback()
        print(f"Error uploading profile picture: {e}")
        flash('Error uploading profile picture. Please try again.', 'error')
    finally:
        cursor.close()
    # Force reload to show new profile picture
    return redirect(url_for('donor.donor_profile'))

@bp.route('/api/donation_details/<int:donation_id>')
@login_required
def get_donation_details(donation_id):
    """API endpoint to get donation details"""
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

@bp.route('/feedback')
@login_required
def donor_feedback():
    """Donor feedback page"""
    donor_id = g.user['id']
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name FROM donor WHERE donor_id = %s", (donor_id,))
        donor = cursor.fetchone()
        name = donor['name'] if donor else 'Donor'
        return render_template('feedback.html', user_type='donor', name=name)
    except Exception as e:
        print(f"Error getting donor info for feedback: {e}")
        return render_template('feedback.html', user_type='donor', name='Donor')
    finally:
        cursor.close()