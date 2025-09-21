from flask import Flask, render_template
import os
from rapid.db import get_bd

def create_app(test_config=None):
    #create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = {
            'host':'localhost',
            'user':'flaskuser',
            'password':'flask',
            'database':'project2' #the name of the database, do not get confused with DATABASE map
        }
    )

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #otherwise load the test config that has been passed to create_app() function
        app.config.from_mapping(
            test_config
        )

    #make sure the instance folder exists
    #this is improtant as all configuration 
    #files are relative to instance folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # TURN DEBUGING OFF BEFORE LAUNCING IN PRODUCTION
    #app.config['DEBUG'] = False
    app.config['DEBUG'] = True

    # Add zip function to Jinja2 environment
    app.jinja_env.globals.update(zip=zip)

    #register the databse connection
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import recipient
    app.register_blueprint(recipient.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from .import donor
    app.register_blueprint(donor.bp)

    from . import volunteer
    app.register_blueprint(volunteer.bp)
    
    @app.route('/')
    def index():
        db = get_bd()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            'SELECT item_id_list FROM donation_receiver'
        )
        all_items = cursor.fetchall()
        #print(all_items)
        cnt = 0
        for entry in all_items:
            items = entry['item_id_list'].split('$')
            
            for item in items:
                item_parts = item.split('#')
                if(len(item) > 0):
                    item_id = item_parts[0]
                    item_name = item_parts[1]
                    item_quantity = item_parts[2]
                    cnt += int(item_quantity)
        cursor.execute(
            'SELECT COUNT(receiver_id) AS cnt FROM receiver'
        )
        receiver_count = cursor.fetchone()['cnt']

        cursor.execute(
            """SELECT COUNT(volunteer_id ) AS v_cnt FROM volunteer
            WHERE status != 'new'"""
        )
        volunteer_count = cursor.fetchone()['v_cnt']

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
        donation_map = {row['month']: row['donation_count'] for row in raw_donations}
        donations_by_month = []
        for month in months:
            donations_by_month.append({
                'month': month,
                'donation_count': donation_map.get(month, 0)
            })

        # Sort by month ascending
        donations_by_month.sort(key=lambda x: x['month'])

        cursor.execute(
            """SELECT SUM(amount) AS money FROM money_transfer"""
        )
        total_donation = cursor.fetchone()['money']

        
        # create this view before running the query

        # CREATE VIEW receiver_by_area_view AS
        # SELECT r.address AS address, COUNT(d.donation_receiver_id)  AS cnt
        # FROM donation_receiver d
        # JOIN receiver r ON d.receiver_id = r.receiver_id
        # GROUP BY r.address;

        cursor.execute(
            """SELECT * FROM receiver_by_area_view"""
        )
        raw_requests_by_area = cursor.fetchall()
        for entry in raw_requests_by_area:
            address = entry['address']
            donation_count = entry['cnt']
            
        requests_by_area = {entry['address']: entry['cnt'] for entry in raw_requests_by_area}

        # CREATE TRIGGER trigger_name
        # AFTER INSERT ON donation_receiver
        # FOR EACH ROW BEGIN
        #     INSERT INTO maping (latitude, longitude) VALUES (NEW.latitude, NEW.longitude);
        # END;

        # CREATE VIEW maping
        # AS
        # SELECT latitude, longitude FROM donation_receiver 
        
        cursor.execute("SELECT * FROM maping")
        map_data = cursor.fetchall()
        print("Map Data:", map_data)  # Debugging line to check map data



        data = {
            'total_items': cnt,
            'total_receivers': receiver_count,
            'total_volunteers': volunteer_count,
            'donations_by_month': donations_by_month,
            'total_donation': total_donation,
            'requests_by_area': requests_by_area,
        }
        return render_template('index.html', data=data, map_data=map_data)
    
    @app.route('/request_donation')
    def request_donation():
        return render_template('request_donation.html')
    return app