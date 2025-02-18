from database.db_connection import get_db_connection
from models.course_model import Course
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import random

def get_all_courses():
    """Fetch all courses from the database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM courses LIMIT 100")
    courses = [Course(**row).to_dict() for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    return courses

def get_course_by_keyword(keyword, user_email=None):
    """Fetch courses matching a keyword and store search history if logged in."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ If user is logged in, store search history
    if user_email:
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
        user = cursor.fetchone()
        if user:
            cursor.execute("INSERT INTO search_history (user_id, keyword) VALUES (%s, %s)", (user["id"], keyword))
            conn.commit()

    # ✅ Fetch courses
    query = "SELECT * FROM courses WHERE title LIKE %s LIMIT 10"
    cursor.execute(query, (f"%{keyword}%",))
    courses = cursor.fetchall()

    cursor.close()
    conn.close()
    return [Course(**row).to_dict() for row in courses]


def get_random_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses")  # Fetch all courses
    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    # ✅ Shuffle courses and pick 20 random ones
    random.shuffle(courses)
    random_courses = courses[:20]

    return [Course(
        id=row["id"],
        topic=row["topic"],
        course_id=row["course_id"],
        title=row["title"],
        url=row["url"],
        thumbnail=row["thumbnail"],
        instructor=row["instructor"],
        instructor_photo=row["instructor_photo"],  # ✅ New column
        num_lectures=row["num_lectures"],  # ✅ New column
        subscribers=row["subscribers"],
        price=row["price"],
        currency=row["currency"],  # ✅ New column
        duration=row["duration"],
        rating=row["rating"],
        description=row["description"]
    ).to_dict() for row in random_courses]

def get_courses_by_subject(topic):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Query to filter courses based on the topic
    query = "SELECT * FROM courses WHERE topic = %s LIMIT 15"
    cursor.execute(query, (topic,))

    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    # ✅ Convert fetched courses into a list of Course objects
    return [Course(
        id=row["id"],
        topic=row["topic"],  # ✅ Updated from "subject"
        course_id=row["course_id"],
        title=row["title"],
        url=row["url"],
        thumbnail=row["thumbnail"],
        instructor=row["instructor"],
        instructor_photo=row["instructor_photo"],  # ✅ New column
        num_lectures=row["num_lectures"],  # ✅ New column
        subscribers=row["subscribers"],
        price=row["price"],
        currency=row["currency"],  # ✅ New column
        duration=row["duration"],
        rating=row["rating"],
        description=row["description"]
    ).to_dict() for row in courses]

def get_course_by_id(course_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM courses WHERE course_id = %s"
    cursor.execute(query, (course_id,))

    course = cursor.fetchone()  # ✅ Fetch a single course

    cursor.close()
    conn.close()

    if course:
        return Course(
            id=course["id"],
            topic=course["topic"],  # ✅ Updated from "subject"
            course_id=course["course_id"],
            title=course["title"],
            url=course["url"],
            thumbnail=course["thumbnail"],
            instructor=course["instructor"],
            instructor_photo=course["instructor_photo"],  # ✅ New column
            num_lectures=course["num_lectures"],  # ✅ New column
            subscribers=course["subscribers"],
            price=course["price"],
            currency=course["currency"],  # ✅ New column
            duration=course["duration"],
            rating=course["rating"],
            description=course["description"]
        ).to_dict()
    
    return None  # ✅ Return None if course is not found

def get_courses_by_instructor(instructor_name):
    """Fetch courses taught by the same instructor."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Query to fetch courses by instructor name
    query = "SELECT * FROM courses WHERE instructor = %s LIMIT 10"
    cursor.execute(query, (instructor_name,))

    courses = cursor.fetchall()
    print(f"🔍 Debug: Found {len(courses)} courses by {instructor_name}")  # ✅ Debug Print

    # ✅ Convert fetched courses into Course objects
    courses_list = [Course(
        id=row["id"],
        topic=row["topic"],
        course_id=row["course_id"],
        title=row["title"],
        url=row["url"],
        thumbnail=row["thumbnail"],
        instructor=row["instructor"],
        instructor_photo=row["instructor_photo"],  
        num_lectures=row["num_lectures"],  
        subscribers=row["subscribers"],
        price=row["price"],
        currency=row["currency"],  
        duration=row["duration"],
        rating=row["rating"],
        description=row["description"]
    ).to_dict() for row in courses]

    cursor.close()
    conn.close()
    return courses_list



