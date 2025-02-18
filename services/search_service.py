from database.db_connection import get_db_connection
from models.course_model import Course
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import random

def get_user_searches(user_email):
    """Fetch the most searched keywords by a user."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Get user_id from email
    cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
    user = cursor.fetchone()
    if not user:
        return []

    user_id = user["id"]

    # ✅ Fetch top 5 most searched keywords
    cursor.execute("""
        SELECT keyword, COUNT(keyword) AS search_count 
        FROM search_history 
        WHERE user_id = %s 
        GROUP BY keyword 
        ORDER BY search_count DESC 
        LIMIT 5
    """, (user_id,))

    searches = [row["keyword"] for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return searches


def get_recommended_courses(user_email):
    """Recommend courses based on user's past searches."""
    searched_keywords = get_user_searches(user_email)
    if not searched_keywords:
        return []  # No recommendations if no searches

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Fetch courses matching user's searched topics
    query = """
        SELECT * FROM courses 
        WHERE title LIKE %s OR title LIKE %s OR title LIKE %s
        LIMIT 10
    """
    cursor.execute(query, tuple([f"%{kw}%" for kw in searched_keywords] + [""] * (3 - len(searched_keywords))))
    
    courses = cursor.fetchall()
    cursor.close()
    conn.close()

    return [Course(**row).to_dict() for row in courses]

def get_trending_searches():
    """Get top 5 trending searches from logged-in users' search history."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Count the most searched keywords
    cursor.execute("""
        SELECT keyword, COUNT(keyword) AS search_count 
        FROM search_history 
        GROUP BY keyword 
        ORDER BY search_count DESC 
        LIMIT 5
    """)

    trending_keywords = [row["keyword"] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    return trending_keywords

def get_trending_courses():
    """Get courses based on trending searches."""
    trending_keywords = get_trending_searches()
    if not trending_keywords:
        return []  # No trending searches available

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Fetch courses matching the trending keywords
    query = "SELECT * FROM courses WHERE " + " OR ".join(["title LIKE %s"] * len(trending_keywords)) + " LIMIT 15"
    cursor.execute(query, tuple(f"%{kw}%" for kw in trending_keywords))
    courses = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return [Course(**row).to_dict() for row in courses]