from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Simple in-memory user storage
users = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('welcome'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            return render_template('login.html', msg='Please fill all fields')

        # Check if user exists and password matches
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['email'] = users[username]['email']
            return redirect(url_for('welcome'))
        else:
            return render_template('login.html', msg='Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        email = request.form.get('email', '').strip()

        if not username or not password or not email:
            return render_template('registration.html', msg='All fields are required')

        if username in users:
            return render_template('registration.html', msg='Username already taken')

        # Simple email validation
        if '@' not in email or '.' not in email:
            return render_template('registration.html', msg='Invalid email')

        # Store user
        users[username] = {
            'password': password,
            'email': email
        }

        return render_template('login.html', msg='Registration successful! Please login.')

    return render_template('registration.html')

@app.route('/welcome')
@login_required
def welcome():
    return render_template('index.html',
                         name=session.get('username', 'User'),
                         msg='Successfully logged in')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', msg='You have been logged out')

if __name__ == '__main__':
    app.run(debug=True)