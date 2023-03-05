from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# Dummy data for testing purposes
SLOTS = {
    1: {'day_of_week': 1, 'start_time': '08:00', 'end_time': '10:00'},
    2: {'day_of_week': 1, 'start_time': '10:00', 'end_time': '12:00'},
    3: {'day_of_week': 2, 'start_time': '08:00', 'end_time': '10:00'},
    4: {'day_of_week': 2, 'start_time': '10:00', 'end_time': '12:00'}
}

FACULTIES = {
    1: {'name': 'John Doe', 'department': 'Computer Science', 'email': 'johndoe@example.com'},
    2: {'name': 'Jane Smith', 'department': 'Physics', 'email': 'janesmith@example.com'}
}

COURSES = {
    1: {'name': 'Introduction to Computer Science', 'description': 'An introductory course in computer science'},
    2: {'name': 'Introduction to Physics', 'description': 'An introductory course in physics'}
}

COURSE_SLOTS = {
    1: {'course_id': 1, 'slot_id': 1, 'faculty_id': 1},
    2: {'course_id': 2, 'slot_id': 3, 'faculty_id': 2},
    3: {'course_id': 1, 'slot_id': 2, 'faculty_id': 1}
}

STUDENTS = {
    1: {'name': 'Alice', 'email': 'alice@example.com', 'password': 'password'},
    2: {'name': 'Bob', 'email': 'bob@example.com', 'password': 'password'}
}

STUDENT_COURSES = {
    1: {'student_id': 1, 'course_slot_id': 1},
    2: {'student_id': 2, 'course_slot_id': 3}
}

# Helper functions for validating requests
def validate_course_slot(course_slot_id):
    if course_slot_id not in COURSE_SLOTS:
        abort(400, message=f"Course slot with ID {course_slot_id} does not exist")

def validate_student_course(student_id, course_slot_id):
    if student_id not in STUDENTS:
        abort(400, message=f"Student with ID {student_id} does not exist")
    if course_slot_id not in COURSE_SLOTS:
        abort(400, message=f"Course slot with ID {course_slot_id} does not exist")
    if STUDENT_COURSES.get(student_id):
        registered_course_slots = [sc['course_slot_id'] for sc in STUDENT_COURSES.values() if sc['student_id'] == student_id]
        for registered_course_slot_id in registered_course_slots:
            if COURSE_SLOTS[registered_course_slot_id]['slot_id'] == COURSE_SLOTS[course_slot_id]['slot_id']:
                abort(400, message=f"Course slot with ID {course_slot_id} does not exist")