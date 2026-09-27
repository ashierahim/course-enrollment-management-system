import database
import sqlite3

def create_course(course_code, course_name, description, credits, instructor_id):
    try:
        query = """
            INSERT INTO courses (course_code, course_name, description, credits, instructor_id)
            VALUES (?, ?, ?, ?, ?)
        """
        course_id = database.execute_query(query, (course_code, course_name, description, credits, instructor_id), commit=True)
        return True, course_id
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e) and "course_code" in str(e):
            return False, "Course code already exists."
        elif "FOREIGN KEY" in str(e):
            return False, "Instructor ID does not exist."
        return False, "Database constraint error."
    except Exception as e:
        return False, str(e)

def get_all_courses():
    return database.execute_query("SELECT * FROM courses")

def get_course_by_id(course_id):
    return database.execute_fetchone("SELECT * FROM courses WHERE course_id = ?", (course_id,))

def update_course(course_id, course_code, course_name, description, credits, instructor_id):
    try:
        query = """
            UPDATE courses 
            SET course_code = ?, course_name = ?, description = ?, credits = ?, instructor_id = ?
            WHERE course_id = ?
        """
        database.execute_query(query, (course_code, course_name, description, credits, instructor_id, course_id), commit=True)
        return True, "Course updated successfully."
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e) and "course_code" in str(e):
            return False, "Course code already exists."
        elif "FOREIGN KEY" in str(e):
            return False, "Instructor ID does not exist."
        return False, "Database constraint error."
    except Exception as e:
        return False, str(e)

def delete_course(course_id):
    try:
        database.execute_query("DELETE FROM courses WHERE course_id = ?", (course_id,), commit=True)
        return True, "Course deleted successfully."
    except Exception as e:
        return False, str(e)
