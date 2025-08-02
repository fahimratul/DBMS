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
        return render_template('signupform.html', role=role)
    else:
        return render_template('login.html', error="Please select a role to continue.")

if __name__ == '__main__':
    app.run(debug=True)
