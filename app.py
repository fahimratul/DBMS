from flask import Flask , render_template , url_for , request

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

@app.route('/admin')
def admin():
    return render_template('admin/admin.html')
@app.route('/admin/events')
def admin_events():
    return render_template('admin/events.html')
if __name__ == '__main__':
    app.run(debug=True)
