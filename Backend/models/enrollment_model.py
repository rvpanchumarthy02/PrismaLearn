from config.db import db
from datetime import datetime
from bson.objectid import ObjectId

class Enrollment:
    @staticmethod
    def enroll_student(user_id, course_id):
        # Relational Check: ensure course exists
        if not db.courses.find_one({"_id": ObjectId(course_id)}):
            return "COURSE_NOT_FOUND"

        # Check Duplication: Has student already enrolled in this course?
        existing_enrollment = db.enrollments.find_one({
            "user_id": ObjectId(user_id),
            "course_id": ObjectId(course_id)
        })

        if existing_enrollment:
            return "ALREADY_ENROLLED"

        new_enrollment = {
            "user_id": ObjectId(user_id),
            "course_id": ObjectId(course_id),
            "enrolled_at": datetime.utcnow(),
            "status": "active"
        }
        
        result = db.enrollments.insert_one(new_enrollment)
        return str(result.inserted_id)

    @staticmethod
    def get_student_enrollments(user_id):
        # Using Aggregation Pipeline to join Enrollments with Courses (Lookups)
        pipeline = [
            {"$match": {"user_id": ObjectId(user_id)}},
            {"$lookup": {
                "from": "courses",
                "localField": "course_id",
                "foreignField": "_id",
                "as": "course_details"
            }},
            {"$unwind": "$course_details"},
            {"$project": {
                "_id": 1,
                "enrolled_at": 1,
                "course_title": "$course_details.title",
                "course_desc": "$course_details.description",
                "instructor": "$course_details.instructor"
            }}
        ]
        
        results = list(db.enrollments.aggregate(pipeline))
        for res in results:
            res['_id'] = str(res['_id'])
        return results