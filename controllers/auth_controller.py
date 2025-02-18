from flask import Blueprint, request, jsonify
from services.auth_service import register_user,authenticate_user

auth_bp = Blueprint('auth_bp', __name__)

# User Registration Route
@auth_bp.route('/register', methods=['POST'])
def register():
    """API endpoint to register a new user."""
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    fullname = data.get("fullname")
    contact = data.get("contact")

    if not username or not email or not password or not fullname or not contact:
        return jsonify({"error": "All fields are required"}), 400

    return jsonify(register_user(username, email, password, fullname, contact))

@auth_bp.route('/login', methods=['POST'])
def login():
    """API endpoint for user login."""
    data = request.get_json()

    # ✅ Check if required fields are provided
    if "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    response, status_code = authenticate_user(data["email"], data["password"])
    return jsonify(response), status_code