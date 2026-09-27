import database
import sqlite3

def create_instructor(user_id, name, email, department):
    try:
        query = """
            INSERT INTO instructors (user_id, name, email, department)
            VALUES (?, ?, ?, ?)
        """
        instructor_id = database.execute_query(query, (user_id, name, email, department), commit=True)
        return True, instructor_id
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e) and "email" in str(e):
            return False, "Email already exists."
        elif "UNIQUE" in str(e) and "user_id" in str(e):
            return False, "This user is already registered as an instructor."
        return False, "Database constraint error."
    except Exception as e:
        return False, str(e)

def get_all_instructors():
    return database.execute_query("SELECT * FROM instructors")

def get_instructor_by_id(instructor_id):
    return database.execute_fetchone("SELECT * FROM instructors WHERE instructor_id = ?", (instructor_id,))

def get_instructor_by_user_id(user_id):
    return database.execute_fetchone("SELECT * FROM instructors WHERE user_id = ?", (user_id,))

def update_instructor(instructor_id, name, email, department):
    try:
        query = """
            UPDATE instructors 
            SET name = ?, email = ?, department = ?
            WHERE instructor_id = ?
        """
        database.execute_query(query, (name, email, department, instructor_id), commit=True)
        return True, "Instructor updated successfully."
    except sqlite3.IntegrityError:
        return False, "Email already exists."
    except Exception as e:
        return False, str(e)

def delete_instructor(instructor_id):
    try:
        database.execute_query("DELETE FROM instructors WHERE instructor_id = ?", (instructor_id,), commit=True)
        return True, "Instructor deleted successfully."
    except Exception as e:
        return False, str(e)
