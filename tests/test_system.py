import unittest
import os
import sqlite3
import sys

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database
# Redirect database to a test database before importing other modules
database.DATABASE_PATH = os.path.join(database.DATABASE_DIR, 'test_enrollment.db')

import auth
import students
import instructors
import courses
import enrollments

class TestSystem(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Ensure test db is clean
        if os.path.exists(database.DATABASE_PATH):
            os.remove(database.DATABASE_PATH)
        database.init_db()
        
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(database.DATABASE_PATH):
            pass # os.remove(database.DATABASE_PATH)
            
    def setUp(self):
        # Clear tables before each test
        conn = database.get_connection()
        conn.execute("DELETE FROM enrollments")
        conn.execute("DELETE FROM courses")
        conn.execute("DELETE FROM students")
        conn.execute("DELETE FROM instructors")
        conn.execute("DELETE FROM users")
        conn.commit()
        conn.close()

    def test_01_user_registration(self):
        success, uid = auth.register_user("testuser", "password123", "STUDENT")
        self.assertTrue(success)
        
        # Duplicate username should fail
        success2, msg = auth.register_user("testuser", "password456", "STUDENT")
        self.assertFalse(success2)

    def test_02_login(self):
        auth.register_user("admin", "admin123", "ADMIN")
        
        # Valid login
        success, user = auth.login("admin", "admin123")
        self.assertTrue(success)
        self.assertEqual(user['role'], "ADMIN")
        
        # Invalid login
        success, msg = auth.login("admin", "wrongpassword")
        self.assertFalse(success)

    def test_03_role_authorization(self):
        auth.register_user("staff", "staff123", "STAFF")
        auth.login("staff", "staff123")
        
        self.assertTrue(auth.require_role(['STAFF', 'ADMIN']))
        self.assertFalse(auth.require_role(['ADMIN']))

    def test_04_student_crud(self):
        auth.register_user("student1", "pass", "STUDENT")
        success, user = auth.login("student1", "pass")
        user_id = user['id']
        
        # Create
        success, s_id = students.create_student(user_id, "John Doe", "john@example.com", "123", "CS", 1)
        self.assertTrue(success)
        
        # Retrieve
        student = students.get_student_by_id(s_id)
        self.assertIsNotNone(student)
        self.assertEqual(student['name'], "John Doe")
        
        # Update
        success, msg = students.update_student(s_id, "John Smith", "john@example.com", "123", "CS", 2)
        self.assertTrue(success)
        student = students.get_student_by_id(s_id)
        self.assertEqual(student['name'], "John Smith")
        
        # Delete
        success, msg = students.delete_student(s_id)
        self.assertTrue(success)
        student = students.get_student_by_id(s_id)
        self.assertIsNone(student)

    def test_05_instructor_crud(self):
        auth.register_user("inst1", "pass", "STAFF")
        _, user = auth.login("inst1", "pass")
        
        # Create
        success, i_id = instructors.create_instructor(user['id'], "Dr. Smith", "smith@example.com", "CS")
        self.assertTrue(success)
        
        # Read
        inst = instructors.get_instructor_by_id(i_id)
        self.assertEqual(inst['name'], "Dr. Smith")
        
        # Update
        instructors.update_instructor(i_id, "Dr. John Smith", "smith@example.com", "CS")
        inst = instructors.get_instructor_by_id(i_id)
        self.assertEqual(inst['name'], "Dr. John Smith")
        
        # Delete
        instructors.delete_instructor(i_id)
        self.assertIsNone(instructors.get_instructor_by_id(i_id))

    def test_06_course_crud(self):
        # Create
        success, c_id = courses.create_course("CS101", "Intro to CS", "Desc", 3, None)
        self.assertTrue(success)
        
        # Duplicate course code
        success2, msg = courses.create_course("CS101", "Another", "Desc", 4, None)
        self.assertFalse(success2)
        
        # Retrieve
        course = courses.get_course_by_id(c_id)
        self.assertEqual(course['course_code'], "CS101")
        
        # Delete
        courses.delete_course(c_id)
        self.assertIsNone(courses.get_course_by_id(c_id))

    def test_07_enrollment_and_constraints(self):
        # Setup User -> Student
        auth.register_user("s1", "pass", "STUDENT")
        _, user = auth.login("s1", "pass")
        _, s_id = students.create_student(user['id'], "Alice", "alice@test.com", "1", "IT", 1)
        
        # Setup Course
        _, c_id = courses.create_course("IT101", "IT Basics", "", 3, None)
        
        # Enroll
        success, e_id = enrollments.enroll_student(s_id, c_id)
        self.assertTrue(success)
        
        # Duplicate enrollment should fail
        success2, msg = enrollments.enroll_student(s_id, c_id)
        self.assertFalse(success2)
        
        # Invalid student should fail due to foreign key
        success3, msg = enrollments.enroll_student(999, c_id)
        self.assertFalse(success3)

    def test_08_error_handling(self):
        # Attempt to create a student with a non-existent user_id
        success, msg = students.create_student(9999, "Ghost", "ghost@example.com", "1", "Ghost", 1)
        self.assertFalse(success)
        self.assertEqual(msg, "Database constraint error.")

if __name__ == '__main__':
    unittest.main()
