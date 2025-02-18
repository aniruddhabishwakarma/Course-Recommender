from flask import Blueprint, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, jwt_required
from services.search_service import get_recommended_courses,get_trending_courses,get_trending_searches

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/courses/search-recommendations', methods=['GET'])
@jwt_required()
def recommend_courses():
    """API to get recommended courses based on user's past searches."""
    user_email = get_jwt_identity()  # ✅ Get logged-in user
    recommended_courses = get_recommended_courses(user_email)
    
    return jsonify(recommended_courses)

@search_bp.route('/courses/trending', methods=['GET'])
def trending_courses():
    """API to get trending searches and recommended courses. No authentication required."""
    trending_keywords = get_trending_searches()
    trending_courses = get_trending_courses()
    
    return jsonify({
        "trending_searches": trending_keywords,
        "recommended_courses": trending_courses
    })