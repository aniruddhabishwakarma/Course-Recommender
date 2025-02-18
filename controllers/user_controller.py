import os
from flask import jsonify, Blueprint,request,send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import get_user_by_email, update_profile_picture
from config.config import UPLOAD_FOLDER

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user/me', methods=['GET'])
@jwt_required()  # ✅ Require authentication
def get_user_info():
    """Fetch the logged-in user's info."""
    user_email = get_jwt_identity()  # ✅ Get user's email from JWT token
    user_data = get_user_by_email(user_email)  # ✅ Fetch user details from DB

    if not user_data:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user_data), 200  # ✅ Return user details

# ✅ Route to update profile picture
@user_bp.route('/user/update-profile-picture', methods=['PATCH'])
@jwt_required()
def upload_profile_picture():
    """API to upload and update profile picture for logged-in user."""
    
    user_email = get_jwt_identity()  # ✅ Get email from JWT Token
    if "profile_picture" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["profile_picture"]
    response, status_code = update_profile_picture(user_email, file)
    
    return jsonify(response), status_code

@user_bp.route('/uploads/<filename>', methods=['GET'])
def get_profile_picture(filename):
    """Serve the user's profile picture."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(UPLOAD_FOLDER, filename)









