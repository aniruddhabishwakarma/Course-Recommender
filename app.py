from flask import Flask, render_template, redirect, url_for, request, session
from controllers import auth_bp, course_bp, search_bp, user_bp
from services.auth_service import bcrypt
from config.jwt_config import init_jwt

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

# Initialize JWT authentication
jwt = init_jwt(app)

# Initialize Bcrypt for password hashing
bcrypt.init_app(app)

# Register Blueprints (Modular Routes)
app.register_blueprint(course_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(search_bp)
app.register_blueprint(user_bp)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Dummy authentication (Replace with DB check)
        if username == "admin" and password == "password":
            session['user'] = username  # Store session
            return redirect(url_for('home'))
        else:
            return "Invalid credentials, please try again."

    return render_template('login.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password (Store in DB instead)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Dummy user creation (Replace with DB insert)
        print(f"User created: {username}, Password: {hashed_password}")

        return redirect(url_for('login'))

    return render_template('signup.html')

# Protected Home Route (Requires Login)
@app.route('/')
def home():
    return render_template('index.html')  # Pass user data

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting the server: {e}")
