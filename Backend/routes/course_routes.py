from flask import Blueprint, request
from models.course_model import Course
from utils.error_handler import success_response, error_response
from middleware.auth_middleware import token_required

course_bp = Blueprint('course', __name__)

@course_bp.route('/', methods=['GET'])
def list_courses():
    courses = Course.get_all_courses()
    return success_response(courses, "Courses retrieved successfully")

# Protected route: Only logged in users can create courses (for MVP simplicity)
@course_bp.route('/', methods=['POST'])
@token_required
def create_course():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    instructor = data.get('instructor')

    if not title or not description:
        return error_response("Missing title or description", 400)

    course_id = Course.create_course(title, description, instructor)
    
    if not course_id:
        return error_response("Course with this title already exists", 409)

    return success_response({"course_id": str(course_id)}, "Course created successfully", 201)