import database
import sqlite3

def enroll_student(student_id, course_id):
    try:
        query = """
            INSERT INTO enrollments (student_id, course_id)
            VALUES (?, ?)
        """
        enrollment_id = database.execute_query(query, (student_id, course_id), commit=True)
        return True, enrollment_id
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e):
            return False, "Student is already enrolled in this course."
        elif "FOREIGN KEY" in str(e):
            return False, "Invalid Student ID or Course ID."
        return False, "Database constraint error."
    except Exception as e:
        return False, str(e)

def get_all_enrollments():
    return database.execute_query("SELECT * FROM enrollments")

def get_enrollment_by_id(enrollment_id):
    return database.execute_fetchone("SELECT * FROM enrollments WHERE enrollment_id = ?", (enrollment_id,))

def get_enrollments_by_student(student_id):
    return database.execute_query("SELECT * FROM enrollments WHERE student_id = ?", (student_id,))

def update_enrollment_status_grade(enrollment_id, status, grade):
    try:
        query = """
            UPDATE enrollments 
            SET status = ?, grade = ?
            WHERE enrollment_id = ?
        """
        database.execute_query(query, (status, grade, enrollment_id), commit=True)
        return True, "Enrollment updated successfully."
    except Exception as e:
        return False, str(e)

def delete_enrollment(enrollment_id):
    try:
        database.execute_query("DELETE FROM enrollments WHERE enrollment_id = ?", (enrollment_id,), commit=True)
        return True, "Enrollment deleted successfully."
    except Exception as e:
        return False, str(e)
