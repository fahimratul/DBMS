from flask import Flask, render_template, request
import os

def create_app(test_config=None):
    #create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = {
            'host':'localhost',
            'user':'root',
            'password':'LongLive@1',
            'database':'dbms' #the name of the database, do not get confused with DATABASE map
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

    # TURN DEBUGING OFF BEFORE LAUNCING
    app.config['DEBUG'] = True

    #register the databse connection
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)




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
            email,
            phone,
            dob,
            address,
            address_2,
            profile_img,
            nid_img,
            username,
            password
        ]
        return render_template('signup/success.html', volunteer_info=volunteer_info)
    return render_template('signup/volunteer_signup.html')

if __name__ == '__main__':
    app.run(debug=True)
