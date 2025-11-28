from flask import Blueprint, request
from models.enrollment_model import Enrollment
from utils.error_handler import success_response, error_response
from middleware.auth_middleware import token_required

enrollment_bp = Blueprint('enrollment', __name__)

@enrollment_bp.route('/enroll', methods=['POST'])
@token_required
def enroll_in_course():
    data = request.json
    course_id = data.get('course_id')
    
    # user_id comes from the token middleware
    user_id = request.user_id 

    if not course_id:
        return error_response("Course ID is required", 400)

    result = Enrollment.enroll_student(user_id, course_id)

    if result == "COURSE_NOT_FOUND":
        return error_response("Course not found", 404)
    if result == "ALREADY_ENROLLED":
        return error_response("You are already enrolled in this course", 409)

    return success_response({"enrollment_id": result}, "Enrolled successfully", 201)

@enrollment_bp.route('/my-courses', methods=['GET'])
@token_required
def get_my_courses():
    user_id = request.user_id
    enrollments = Enrollment.get_student_enrollments(user_id)
    return success_response(enrollments, "Enrollments retrieved successfully")