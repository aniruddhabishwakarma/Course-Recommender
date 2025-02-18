import os

DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "LEapfrog@33",
    "database": "course_recommendation"
}

# Define the upload folder path
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)