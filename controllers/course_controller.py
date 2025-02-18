from flask import Blueprint, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, jwt_required
from services.course_service import get_all_courses, get_random_courses, get_courses_by_subject
from services.course_service import get_course_by_keyword, get_course_by_id, get_courses_by_instructor
from services.recommendation_service import get_similar_courses


course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/courses', methods=['GET'])
def fetch_courses():
    """API endpoint to get all courses."""
    courses = get_all_courses()
    return jsonify(courses)



@course_bp.route('/courses/random', methods=['GET'])
def fetch_random_courses():
    """API endpoint to get 100 random courses."""
    courses = get_random_courses()
    return jsonify(courses)


@course_bp.route('/courses/subject', methods=['GET'])
def fetch_courses_by_subject():
    """API endpoint to get courses filtered by subject."""
    subject = request.args.get('subject', '')

    if not subject:
        return jsonify({"error": "Subject parameter is required"}), 400

    courses = get_courses_by_subject(subject)
    return jsonify(courses)

@course_bp.route('/courses/search', methods=['GET'])
def search_courses():
    """API to search courses. Stores search history only if logged in."""
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    # ✅ Try to verify if user is logged in (JWT Token present)
    user_email = None
    try:
        verify_jwt_in_request(optional=True)  # ✅ Allows API to work without JWT
        user_email = get_jwt_identity()  # ✅ Get logged-in user
    except Exception:
        pass  # ✅ No JWT, continue as a guest

    courses = get_course_by_keyword(keyword, user_email)
    return jsonify(courses)


@course_bp.route('/courses/<int:course_id>', methods=['GET'])
def fetch_course_by_id(course_id):
    """API endpoint to get a single course by ID."""
    course = get_course_by_id(course_id)

    if not course:
        return jsonify({"error": "Course not found"}), 404

    return jsonify(course)

@course_bp.route('/courses/instructor', methods=['GET'])
def fetch_courses_by_instructor():
    instructor_name = request.args.get('instructor')  # ✅ Get instructor from query params
    if not instructor_name:
        return jsonify({"error": "Instructor name is required"}), 400

    courses = get_courses_by_instructor(instructor_name)
    return jsonify(courses)

@course_bp.route('/courses/recommend', methods=['GET'])
@jwt_required()  # ✅ Require authentication
def recommend_courses():
    """API to get recommended courses based on user's past searches."""
    user_email = get_jwt_identity()  # ✅ Get logged-in user's email
    
    # ✅ Get course_id from query parameter
    course_id = request.args.get("course_id")
    
    if not course_id:
        return jsonify({"error": "Missing course_id parameter"}), 400

    try:
        recommended_courses = get_similar_courses(int(course_id))
        return jsonify(recommended_courses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


