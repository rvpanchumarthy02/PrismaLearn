from config.db import db
from datetime import datetime
from bson.objectid import ObjectId

class Course:
    @staticmethod
    def create_course(title, description, instructor):
        # Check if course code/title already exists to avoid duplicates
        if db.courses.find_one({"title": title}):
            return None

        new_course = {
            "title": title,
            "description": description,
            "instructor": instructor,
            "created_at": datetime.utcnow()
        }
        result = db.courses.insert_one(new_course)
        return result.inserted_id

    @staticmethod
    def get_all_courses():
        courses = db.courses.find()
        # Convert ObjectId to string for JSON serialization
        course_list = []
        for course in courses:
            course['_id'] = str(course['_id'])
            course_list.append(course)
        return course_list

    @staticmethod
    def get_course_by_id(course_id):
        try:
            course = db.courses.find_one({"_id": ObjectId(course_id)})
            if course:
                course['_id'] = str(course['_id'])
            return course
        except:
            return None