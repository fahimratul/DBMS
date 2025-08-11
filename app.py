# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'LongLive@1'
app.config['MYSQL_DB'] = 'dbms'


mysql = MySQL(app)



app = Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    role = request.form.get('role')
    if role:
        if role == 'Donor':
            return render_template('signup/donor_signup.html')
        elif role == 'Recipient':
            return render_template('signup/recipient_signup.html')
        elif role == 'Volunteer':
            return render_template('signup/volunteer_signup.html')
        else:
            return render_template('login.html', error="Invalid role selected.")
    return render_template('login.html', error="Role not specified.")

@app.route('/donor')
def donor():
     return render_template('donor/donor.html')
@app.route('/donor/profile')
def profile():
    return render_template('donor/profile.html') 
@app.route('/donor/donate')
def donate():
    return render_template('donor/donate.html') 
@app.route('/donor/history')
def history():
    return render_template('donor/history.html') 


@app.route('/admin')
def admin():
    return render_template('admin/admin.html')
@app.route('/admin/events')
def admin_events():
    return render_template('admin/events.html')
@app.route('/admin/events/create')
def create_event():
    return render_template('admin/create_event.html')

@app.route('/admin/volunteers')
def volunteer_list():
    return render_template('admin/volunteer_list.html')
@app.route('/admin/requests')
def admin_requests():
    return render_template('admin/requests.html')
@app.route('/admin/donors')
def admin_donors():
    return render_template('admin/donor_list.html')
@app.route('/admin/stock')
def admin_stock():
    return render_template('admin/stock.html')

@app.route('/volunteer_signup', methods=['GET', 'POST'])
def volunteer_signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        address = request.form.get('address')
        address_2 = request.form.get('address_2')
        profile_img = request.files.get('profile_img')
        nid_img = request.files.get('nid_img')
        username = request.form.get('username')
        password = request.form.get('password')

        volunteer_info = [
            name,
            phone,
            email,
            dob,
            address,
            address_2,
            username,
            password,
            nid_img,
        ]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO volunteer (name, phone, email, dob, address, pref_address, username, password, nid_birthcert) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", volunteer_info)
        mysql.connection.commit()
        cursor.close()
        return render_template('signup/success.html', volunteer_info=volunteer_info)
    return render_template('signup/volunteer_signup.html')

if __name__ == '__main__':
    app.run(debug=True)