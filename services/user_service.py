from database.db_connection import get_db_connection
import os
from werkzeug.utils import secure_filename
from config.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_by_email(email):
    """Fetch user details by email."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT id, username, email, fullname, contact, thumbnail FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    return user_data if user_data else None

# ✅ Function to update profile picture
def update_profile_picture(user_email, file):
    """Upload and update user profile picture."""

    if not file or not allowed_file(file.filename):
        return {"error": "Invalid file type. Only PNG, JPG, and JPEG are allowed"}, 400

    # Secure filename
    filename = secure_filename(f"{user_email}_{file.filename}")

    # Save file to uploads folder
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Update in database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("UPDATE users SET thumbnail = %s WHERE email = %s", (filename, user_email))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Profile picture updated successfully", "thumbnail": filename}, 200