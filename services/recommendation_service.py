import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database.db_connection import get_db_connection

# ✅ Load Course Data from Database
def load_courses():
    """Fetch all courses from the database and return as DataFrame."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ✅ Ensure 'course_id' is selected from the database
    query = """
        SELECT 
            course_id, title, description, url, thumbnail, instructor, 
            instructor_photo, num_lectures, subscribers, price, currency, 
            duration, rating, topic 
        FROM courses
    """
    cursor.execute(query)  
    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    df = pd.DataFrame(courses)

    # ✅ Ensure 'course_id' column exists
    if "course_id" not in df.columns:
        print("❌ ERROR: 'course_id' column is missing in DataFrame!")
        df["course_id"] = None  # Add empty column as a fallback

    return df

# ✅ Compute Course Similarity Using TF-IDF
def compute_course_similarity():
    """Compute TF-IDF similarity scores between courses."""
    df = load_courses()
    if df.empty:
        return None, None  # No courses available

    # ✅ Vectorize Course Titles & Descriptions
    tfidf = TfidfVectorizer(stop_words="english")
    df["text_features"] = df["title"] + " " + df["description"] + " " + df["topic"]
    tfidf_matrix = tfidf.fit_transform(df["text_features"])

    # ✅ Compute Cosine Similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)

    return df, similarity_matrix

def get_similar_courses(course_id, num_recommendations=10):
    """Recommend similar courses based on Udemy's 'course_id'."""
    df, similarity_matrix = compute_course_similarity()
    
    if df is None or similarity_matrix is None:
        return []

    # ✅ Ensure 'course_id' column is of type string
    df["course_id"] = df["course_id"].astype(str)

    # ✅ Debug: Print available columns
    print("🔍 Available Columns:", df.columns.tolist())

    # ✅ Check if required columns exist
    required_columns = [
        "course_id", "title", "description", "url", "thumbnail", "instructor",
        "instructor_photo", "num_lectures", "subscribers", "price", "currency",
        "duration", "rating"
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"❌ ERROR: Missing Columns - {missing_columns}")
        return []

    # ✅ Find Course Index
    try:
        idx = df[df["course_id"] == str(course_id)].index[0]
    except IndexError:
        print(f"❌ ERROR: Course ID {course_id} not found in DataFrame!")
        return []

    # ✅ Get Similar Courses
    similar_indices = similarity_matrix[idx].argsort()[::-1][1:num_recommendations+1]
    recommended_courses = df.iloc[similar_indices]

    # ✅ Return Full Course Details
    return recommended_courses[required_columns].to_dict(orient="records")