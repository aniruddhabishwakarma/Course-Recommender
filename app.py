
from flask import Flask
from controllers import auth_bp, course_bp, search_bp, user_bp  # Import Blueprints from controllers
from services.auth_service import bcrypt
from config.jwt_config import init_jwt

app = Flask(__name__)

# Initialize JWT
jwt = init_jwt(app)

# Initialize Bcrypt for password hashing
bcrypt.init_app(app)

# Register Blueprints (Modular Routes)
app.register_blueprint(course_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(search_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)