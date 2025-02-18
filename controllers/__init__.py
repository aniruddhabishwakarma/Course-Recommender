from flask import Blueprint

# Create a Blueprint for controllers
course_bp = Blueprint('course_bp', __name__)

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

search_bp= Blueprint('search_bp', __name__)

user_bp = Blueprint('user_bp',__name__)

from .course_controller import *  # Import all controllers
from .auth_controller import *  # Import all authentication controllers
from .search_controller import *
from .user_controller import *