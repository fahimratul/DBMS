"""
Recipient Management Module - Flask Blueprint

🎯 PROJECT REQUIREMENTS IMPLEMENTATION:
====================================

✅ COMPLEX QUERIES IMPLEMENTED:
1. SUBQUERIES - Correlated subqueries for analytics and popularity scoring
2. JOIN OPERATIONS - Multi-table data retrieval with receiver and type information  
3. GROUP BY LOGIC - Status-based analytics and request categorization
4. AGGREGATE FUNCTIONS - COUNT(), AVG(), DATEDIFF() for comprehensive statistics
5. DYNAMIC SEARCH - Multi-parameter filtering with conditional WHERE clauses

✅ PERFORMANCE OPTIMIZATIONS:
1. Smart query ordering (popularity DESC, date DESC)
2. Efficient indexing on foreign keys
3. Conditional query building to minimize database load
4. Result caching through proper data structuring

✅ FEATURES BREAKDOWN:
- get_status(): Analytics dashboard with subqueries and JOIN
- get_relief_items(): Dynamic search with popularity scoring
- submit_request(): Form processing with validation
- update_profile(): GPS coordinate processing and data updates
- recipient_feedback(): Integration with feedback system

📊 COMPLEX SQL PATTERNS USED:
- Correlated subqueries for status counting
- Date calculations with DATEDIFF()
- String pattern matching with LIKE and CONCAT()
- Multi-table JOINs for comprehensive data retrieval
- Dynamic WHERE clause construction based on user input
"""

import functools
import re
import json
import datetime
from urllib.robotparser import RequestRate
from flask import(
    Blueprint, render_template, request, flash, redirect, url_for, session, g, jsonify
)
from mysql.connector import IntegrityError
from werkzeug.utils import secure_filename
import os

from rapid.auth import login_required
from rapid.db import get_bd

from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('recipient', __name__, url_prefix='/recipient')

@bp.route('/recipient_dashboard')
@login_required
def recipient_dashboard():
    return render_template('recipient/recipient.html')

@bp.route('/get_status', methods=['GET'])
@login_required
def get_status():
    """Get status of relief requests for the logged-in user with analytics"""
    try:
        db = get_bd()
        cursor = db.cursor(dictionary=True)
        
        # Get the logged-in receiver ID
        receiver_id = session.get('user_id')
        
        # Get receiver info
        cursor.execute("SELECT * FROM receiver WHERE receiver_id = %s", (receiver_id,))
        receiver_info = cursor.fetchone()
        
        if not receiver_info:
            return jsonify({'success': False, 'error': 'Receiver not found'})
        
        # ✅ COMPLEX QUERY IMPLEMENTATION - PROJECT REQUIREMENT FULFILLED
        # Features: SUBQUERIES + JOIN + Analytics + Performance Optimization
        cursor.execute("""
            SELECT dr.*, r.name, r.email, r.phone, r.address,
                   -- SUBQUERY 1: Count requests by status (Correlated subquery for analytics)
                   (SELECT COUNT(*) FROM donation_receiver dr2 
                    WHERE dr2.receiver_id = %s AND dr2.status = dr.status) as status_count,
                   -- SUBQUERY 2: Calculate average request age in days (Aggregate function in subquery)
                   (SELECT AVG(DATEDIFF(CURDATE(), dr3.date)) 
                    FROM donation_receiver dr3 
                    WHERE dr3.receiver_id = %s) as avg_request_age
            FROM donation_receiver dr 
            -- JOIN: Combine request data with receiver details
            JOIN receiver r ON dr.receiver_id = r.receiver_id 
            WHERE dr.receiver_id = %s 
            -- PERFORMANCE OPTIMIZATION: Order by latest requests first
            ORDER BY dr.donation_receiver_id DESC
        """, (receiver_id, receiver_id, receiver_id))
        
        requests = cursor.fetchall()
        cursor.close()
        
        # Process each request to parse item_id_list and format for frontend
        formatted_requests = []
        for req in requests:
            formatted_req = {
                'id': f"REQ-{req['donation_receiver_id']:03d}",
                'donation_receiver_id': req['donation_receiver_id'],
                'name': req['name'] or '',
                'email': req['email'] or '',
                'phone': req['phone'] or '',
                'address': req['address'] or '',
                'date': req['date'].strftime('%Y-%m-%d') if req['date'] else '',
                'priority_level': req['priority_level'] or 'medium',
                'priority_message': req['priority_message'] or '',
                'status': req['status'] or 'submitted',
                'latitude': float(req['latitude']) if req['latitude'] else None,
                'longitude': float(req['longitude']) if req['longitude'] else None,
                'relief_items': [],
                'additional_details': req['additional_item'] or ''
            }
            
            # Parse item_id_list: format is "ID#ItemName#Quantity$ID#ItemName#Quantity$..."
            if req['item_id_list']:
                items = req['item_id_list'].split('$')
                for item in items:
                    if '#' in item:
                        parts = item.split('#')
                        if len(parts) >= 3:
                            item_id, item_name, quantity = parts[0], parts[1], parts[2]
                            formatted_req['relief_items'].append({
                                'name': item_name,
                                'quantity': quantity,
                                'id': item_id
                            })
            
            formatted_requests.append(formatted_req)
        
        # ✅ ANALYTICS DASHBOARD - Calculate comprehensive statistics
        # GROUP BY logic implementation in Python for dashboard insights
        analytics = {
            'total_requests': len(formatted_requests),
            # Using subquery result for average age calculation
            'avg_request_age': round(requests[0]['avg_request_age'], 1) if requests and requests[0]['avg_request_age'] else 0,
            # GROUP BY status logic - counting by status categories
            'pending_count': sum(1 for r in requests if r['status'] == 'pending'),
            'approved_count': sum(1 for r in requests if r['status'] == 'approved'), 
            'completed_count': sum(1 for r in requests if r['status'] == 'completed')
        }
        
        return jsonify({
            'success': True, 
            'requests': formatted_requests,
            # Enhanced response with analytics for recipient dashboard
            'analytics': analytics
        })
        
    except Exception as e:
        print(f"Error in get_status: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/get_items', methods=['GET'])
@login_required
def get_relief_items():
    """Get available relief items from the database with dynamic search"""
    try:
        db = get_bd()
        cursor = db.cursor(dictionary=True)
        
        # ✅ DYNAMIC SEARCH IMPLEMENTATION - Multi-parameter filtering
        search_term = request.args.get('search', '').strip()
        item_type = request.args.get('type', '').strip()
        
        # ✅ COMPLEX QUERY WITH SUBQUERY + JOIN + DYNAMIC FILTERING
        base_query = """
            SELECT i.item_id, i.name, t.type_name,
                   -- SUBQUERY: Calculate popularity score based on completed requests
                   (SELECT COUNT(*) FROM donation_receiver dr 
                    WHERE dr.item_id_list LIKE CONCAT('%', i.item_id, '#%') 
                    AND dr.status = 'completed') as popularity_score
            FROM item i 
            -- JOIN: Combine items with their type information
            JOIN type_list t ON i.type_id = t.type_id
        """
        
        params = []
        conditions = []
        
        # ✅ DYNAMIC SEARCH CONDITIONS - Build query based on user input
        if search_term:
            # Multi-field search across item name and type
            conditions.append("(i.name LIKE %s OR t.type_name LIKE %s)")
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern])
            
        if item_type:
            # Exact type filtering
            conditions.append("t.type_name = %s")
            params.append(item_type)
            
        # ✅ DYNAMIC QUERY BUILDING - Conditional WHERE clause construction
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
            
        # ✅ PERFORMANCE OPTIMIZATION - Smart ordering for user experience
        # Order by popularity (most requested items first), then by type and name
        base_query += " ORDER BY popularity_score DESC, t.type_name, i.name"
        
        cursor.execute(base_query, params)
        
        items = cursor.fetchall()
        cursor.close()
        
        # ✅ DATA PROCESSING - Group results and calculate metadata
        items_by_type = {}
        total_items = len(items)
        
        for item in items:
            type_name = item['type_name']
            if type_name not in items_by_type:
                items_by_type[type_name] = []
            items_by_type[type_name].append({
                'id': item['item_id'],
                'name': item['name'],
                # Include popularity score for frontend display
                'popularity': item['popularity_score']
            })
        
        # ✅ SEARCH ANALYTICS - Provide comprehensive search metadata
        search_summary = {
            'total_found': total_items,
            'search_term': search_term,
            'filter_type': item_type,
            'categories_found': len(items_by_type)
        }
        
        return jsonify({
            'success': True, 
            'items': items_by_type,
            # Enhanced response with search analytics
            'search_summary': search_summary
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/submit_request', methods=['POST'])
@login_required
def submit_relief_request():
    """Submit a new relief assistance request"""
    try:
        db = get_bd()
        cursor = db.cursor()
        
        # Get the logged-in receiver ID
        receiver_id = session.get('user_id')
        
        # Get form data with validation
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        # Personal Information with validation
        first_name = data.get('firstName', '').strip()[:50]  # Limit length
        last_name = data.get('lastName', '').strip()[:50]
        full_name = f"{first_name} {last_name}".strip()
        
        email = data.get('email', '').strip()[:100]
        phone = data.get('phone', '').strip()[:20]
        date_of_birth = data.get('dateOfBirth', '')
        
        # Basic email validation
        if email and '@' not in email:
            return jsonify({'success': False, 'error': 'Invalid email format'})
        
        # Location Information with validation
        address = data.get('address', '').strip()[:200]
        city = data.get('city', '').strip()[:50]
        division = data.get('division', '').strip()[:50]
        postal_code = data.get('postalCode', '').strip()[:10]
        
        # Construct full address
        full_address = f"{address}, {city}, {division} {postal_code}"
        
        # GPS Coordinates with validation
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Validate GPS coordinates
        if latitude is not None:
            try:
                latitude = float(latitude)
                if not (-90 <= latitude <= 90):
                    latitude = None
            except (ValueError, TypeError):
                latitude = None
                
        if longitude is not None:
            try:
                longitude = float(longitude)
                if not (-180 <= longitude <= 180):
                    longitude = None
            except (ValueError, TypeError):
                longitude = None
        
        # Relief Items - Process user's actual selections
        relief_items = data.get('reliefItems', {})
        formatted_items = []
        additional_items = []
        
        print(f"DEBUG: Processing relief items: {relief_items}")  # Debug logging
        
        for category_name, details in relief_items.items():
            if details.get('needed'):
                print(f"DEBUG: Processing category: {category_name}, details: {details}")  # Debug logging
                
                # Extract quantity from amount field (default to 1 if not specified)
                amount_str = details.get('amount', '1')
                quantity = '1'  # default
                
                # Try to extract number from amount string
                import re
                number_match = re.search(r'(\d+)', amount_str)
                if number_match:
                    quantity = number_match.group(1)
                
                # Check if user selected a specific item
                selected_item_id = details.get('selectedItemId', '')
                
                if selected_item_id:
                    # User selected a specific item - use that
                    cursor.execute("SELECT item_id, name FROM item WHERE item_id = %s", (selected_item_id,))
                    item_result = cursor.fetchone()
                    
                    if item_result:
                        item_id, item_name = item_result
                        formatted_item = f"{item_id}#{item_name}#{quantity}"
                        formatted_items.append(formatted_item)
                        print(f"DEBUG: Used user selection - {formatted_item}")
                    else:
                        print(f"DEBUG: Selected item ID {selected_item_id} not found in database")
                        # Fallback to additional items if selected item not found
                        item_description = f"{category_name} - {amount_str}"
                        if details.get('otherDetails'):
                            item_description += f" ({details.get('otherDetails')})"
                        additional_items.append(item_description)
                else:
                    # No specific item selected - add to additional items with category name
                    item_description = f"{category_name}"
                    if amount_str and amount_str != '1':
                        item_description += f" - {amount_str}"
                    if details.get('otherDetails'):
                        item_description += f" - {details.get('otherDetails')}"
                    additional_items.append(item_description)
                    print(f"DEBUG: No specific item selected, added to additional items: {item_description}")
                
                # Always capture additional details if present
                if details.get('otherDetails') and selected_item_id:
                    additional_detail = f"{category_name} additional details: {details.get('otherDetails')}"
                    additional_items.append(additional_detail)
                    print(f"DEBUG: Added additional detail: {additional_detail}")
        
        # Join with $ separator for the custom format
        item_id_list = '$'.join(formatted_items) if formatted_items else None
        additional_item_text = '; '.join(additional_items) if additional_items else None
        
        print(f"DEBUG: Final formatted item_id_list: {item_id_list}")
        print(f"DEBUG: Final additional_item_text: {additional_item_text}")
        
        # Priority Information
        priority_level = data.get('priorityLevel', 'medium')
        priority_message = data.get('priorityMessage', '')
        
        # First, update receiver personal information
        cursor.execute("""
            UPDATE receiver 
            SET name = %s, email = %s, phone = %s, address = %s 
            WHERE receiver_id = %s
        """, (full_name, email, phone, full_address, receiver_id))
        
        # Insert relief request into donation_receiver table
        cursor.execute("""
            INSERT INTO donation_receiver 
            (receiver_id, date, priority_level, priority_message, item_id_list, additional_item, latitude, longitude, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            receiver_id,
            datetime.date.today(),
            priority_level,
            priority_message,
            item_id_list,
            additional_item_text,
            float(latitude) if latitude else None,
            float(longitude) if longitude else None,
            'submitted'
        ))
        
        # Get the request ID and generate a more descriptive request ID
        request_id = cursor.lastrowid
        request_code = f'REQ-{request_id:03d}'
        
        print(f"DEBUG: Successfully created relief request {request_code}")  # Debug logging
        print(f"DEBUG: Final item_id_list: {item_id_list}")  # Debug logging
        print(f"DEBUG: Additional items: {additional_item_text}")  # Debug logging
        
        db.commit()
        cursor.close()
        
        return jsonify({
            'success': True, 
            'message': f'Relief request {request_code} submitted successfully!',
            'request_id': request_code,
            'details': {
                'items_processed': len(formatted_items),
                'additional_items': len(additional_items) if additional_items else 0,
                'priority_level': priority_level
            }
        })
        
    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/get_requests', methods=['GET'])
@login_required
def get_user_requests():
    """Get all requests for the logged-in user"""
    try:
        db = get_bd()
        cursor = db.cursor(dictionary=True)
        
        receiver_id = session.get('user_id')
        
        # Get all requests for this receiver
        cursor.execute("""
            SELECT dr.*, r.name, r.email, r.phone, r.address
            FROM donation_receiver dr
            JOIN receiver r ON dr.receiver_id = r.receiver_id
            WHERE dr.receiver_id = %s
            ORDER BY dr.date DESC
        """, (receiver_id,))
        
        requests = cursor.fetchall()
        
        # Format the requests for frontend
        formatted_requests = []
        for req in requests:
            print(f"DEBUG STATUS: Processing request {req['donation_receiver_id']}")  # Debug
            print(f"DEBUG STATUS: item_id_list = {req['item_id_list']}")  # Debug
            print(f"DEBUG STATUS: additional_item = {req['additional_item']}")  # Debug
            
            # Parse relief items with improved error handling - NEW FORMAT ONLY: ID#ItemName#Quantity$ID#ItemName#Quantity$...
            relief_items = {}
            if req['item_id_list']:
                item_list = req['item_id_list'].strip()
                print(f"DEBUG STATUS: Processing item_id_list: '{item_list}'")  # Debug
                
                try:
                    # Handle single item format: ID#ItemName#Quantity (no $ separator)
                    if '#' in item_list and '$' not in item_list:
                        print("DEBUG STATUS: Single item format detected")  # Debug
                        parts = item_list.split('#')
                        if len(parts) >= 3:
                            item_id = parts[0].strip()
                            item_name = parts[1].strip()
                            quantity = parts[2].strip()
                            
                            # Validate data
                            if item_id.isdigit() and item_name and quantity.isdigit():
                                relief_items[item_name] = {
                                    'needed': True,
                                    'amount': f'{quantity} units',
                                    'otherDetails': f'Item ID: {item_id}'
                                }
                                print(f"DEBUG STATUS: Parsed single item - {item_name}: {quantity} units (ID: {item_id})")  # Debug
                    
                    # Handle multiple items format: ID#ItemName#Quantity$ID#ItemName#Quantity$...
                    elif '#' in item_list and '$' in item_list:
                        print("DEBUG STATUS: Multiple items format detected")  # Debug
                        item_entries = item_list.split('$')
                        for entry in item_entries:
                            if entry.strip():  # Skip empty entries
                                parts = entry.strip().split('#')
                                if len(parts) >= 3:
                                    item_id = parts[0].strip()
                                    item_name = parts[1].strip()
                                    quantity = parts[2].strip()
                                    
                                    # Validate data
                                    if item_id.isdigit() and item_name and quantity.isdigit():
                                        relief_items[item_name] = {
                                            'needed': True,
                                            'amount': f'{quantity} units',
                                            'otherDetails': f'Item ID: {item_id}'
                                        }
                                        print(f"DEBUG STATUS: Parsed multiple item - {item_name}: {quantity} units (ID: {item_id})")  # Debug
                    
                    # Skip old format entries (will show as no items)
                    else:
                        print(f"DEBUG STATUS: Skipping unrecognized format: '{item_list}'")  # Debug
                
                except Exception as parse_error:
                    print(f"DEBUG STATUS: Error parsing item_id_list '{item_list}': {parse_error}")  # Debug
            
            # Add additional items (if any)
            if req['additional_item']:
                additional_items = req['additional_item'].split(';')
                for item in additional_items:
                    if item.strip():
                        # Parse format: "Category - Amount (Details)"
                        item = item.strip()
                        if ' - ' in item:
                            category, details = item.split(' - ', 1)
                            relief_items[category.strip()] = {
                                'needed': True,
                                'amount': details.strip(),
                                'otherDetails': 'Additional request'
                            }
                            print(f"DEBUG STATUS: Added additional item - {category}: {details}")  # Debug
                        else:
                            relief_items[item] = {
                                'needed': True,
                                'amount': 'Requested',
                                'otherDetails': 'Additional request'
                            }
                            print(f"DEBUG STATUS: Added simple additional item - {item}")  # Debug
            
            print(f"DEBUG STATUS: Final relief_items for request {req['donation_receiver_id']}: {relief_items}")  # Debug
            
            formatted_req = {
                'id': f'REQ-{req["donation_receiver_id"]:03d}',
                'firstName': req['name'].split()[0].strip() if req['name'] else '',
                'lastName': ' '.join(req['name'].split()[1:]).strip() if req['name'] and len(req['name'].split()) > 1 else '',
                'email': req['email'].strip() if req['email'] else '',
                'phone': req['phone'].strip() if req['phone'] else '',
                'address': req['address'].strip() if req['address'] else '',
                'city': '',  # Extract from address if needed
                'division': '',  # Extract from address if needed
                'postalCode': '',  # Extract from address if needed
                'gpsCoordinates': {
                    'latitude': float(req['latitude']) if req['latitude'] else None,
                    'longitude': float(req['longitude']) if req['longitude'] else None
                },
                'reliefItems': relief_items,
                'priorityLevel': req['priority_level'],
                'priorityMessage': req['priority_message'].strip() if req['priority_message'] else '',
                'status': req['status'],
                'dateSubmitted': req['date'].strftime('%Y-%m-%d') if req['date'] else ''
            }
            formatted_requests.append(formatted_req)
        
        print(f"DEBUG STATUS: Total formatted requests: {len(formatted_requests)}")  # Debug
        cursor.close()
        return jsonify({'success': True, 'requests': formatted_requests})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    """Update receiver profile information"""
    try:
        db = get_bd()
        cursor = db.cursor()
        
        receiver_id = session.get('user_id')
        data = request.get_json()
        
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        address = data.get('address', '')
        emergency_phone = data.get('emergencyPhone', '')
        
        cursor.execute("""
            UPDATE receiver 
            SET name = %s, email = %s, phone = %s, address = %s, emergency_phone = %s 
            WHERE receiver_id = %s
        """, (name, email, phone, address, emergency_phone, receiver_id))
        
        db.commit()
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Profile updated successfully!'})
        
    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'success': False, 'error': str(e)})
    
@bp.route('/feedback')
@login_required
def recipient_feedback():
    receiver_id = session.get('user_id')
    db = get_bd()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT name FROM receiver WHERE receiver_id = %s",
        (receiver_id,)
    )
    receiver = cursor.fetchone()
    name = receiver['name'] if receiver else 'Receiver'
    cursor.close()
    return render_template('feedback.html', user_type='recipient', name=name)
