import mysql.connector
import os
from flask_bcrypt import Bcrypt
from models import User
from database.db_connection import get_db_connection
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()

UPLOAD_FOLDER = "uploads"  # Folder to store profile pictures
DEFAULT_PROFILE_PIC =  "default.jpg"  # Default profile picture

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def register_user(username, email, password, fullname, contact):
    """Register a new user."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # ✅ Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (email, username))
        existing_user = cursor.fetchone()
        if existing_user:
            return {"error": "User already exists"}, 400

        # ✅ Hash the password securely
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        # ✅ Insert new user into database
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, fullname, contact, thumbnail) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, email, password_hash, fullname, contact, DEFAULT_PROFILE_PIC))

        conn.commit()
        user_id = cursor.lastrowid  # ✅ Get the new user ID

        # ✅ Fetch the newly created user
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()

        return {"message": "User registered successfully", "user": User(**user_data).to_dict()}, 201

    except Exception as e:
        conn.rollback()  # ✅ Rollback in case of an error
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        conn.close()  # ✅ Ensure connection is closed properly



def authenticate_user(email, password):
    """Authenticate user and return JWT token."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user_data:
        return {"error": "Invalid credentials"}, 401

    user = User(**user_data)

    # Verify password
    if not bcrypt.check_password_hash(user.password_hash, password):
        return {"error": "Invalid credentials"}, 401

    # Generate JWT token
    access_token = create_access_token(identity=user.email)

    return {"token": access_token}, 200  # Return only the token