import database
import sqlite3

def create_student(user_id, name, email, phone, department, year):
    try:
        query = """
            INSERT INTO students (user_id, name, email, phone, department, year)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        student_id = database.execute_query(query, (user_id, name, email, phone, department, year), commit=True)
        return True, student_id
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e) and "email" in str(e):
            return False, "Email already exists."
        elif "UNIQUE" in str(e) and "user_id" in str(e):
            return False, "This user is already registered as a student."
        return False, "Database constraint error."
    except Exception as e:
        return False, str(e)

def get_all_students():
    return database.execute_query("SELECT * FROM students")

def get_student_by_id(student_id):
    return database.execute_fetchone("SELECT * FROM students WHERE student_id = ?", (student_id,))

def get_student_by_user_id(user_id):
    return database.execute_fetchone("SELECT * FROM students WHERE user_id = ?", (user_id,))

def update_student(student_id, name, email, phone, department, year):
    try:
        query = """
            UPDATE students 
            SET name = ?, email = ?, phone = ?, department = ?, year = ?
            WHERE student_id = ?
        """
        database.execute_query(query, (name, email, phone, department, year, student_id), commit=True)
        return True, "Student updated successfully."
    except sqlite3.IntegrityError:
        return False, "Email already exists."
    except Exception as e:
        return False, str(e)

def delete_student(student_id):
    try:
        database.execute_query("DELETE FROM students WHERE student_id = ?", (student_id,), commit=True)
        return True, "Student deleted successfully."
    except Exception as e:
        return False, str(e)
