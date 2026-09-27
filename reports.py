import database

def report_courses_with_instructors():
    """Demonstrates INNER JOIN between courses and instructors."""
    query = """
        SELECT c.course_code, c.course_name, c.credits, i.name AS instructor_name
        FROM courses c
        LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
    """
    return database.execute_query(query)

def report_students_in_course(course_id):
    """Demonstrates INNER JOIN between students and enrollments."""
    query = """
        SELECT s.student_id, s.name, s.email, e.status, e.grade, e.enrollment_date
        FROM students s
        INNER JOIN enrollments e ON s.student_id = e.student_id
        WHERE e.course_id = ?
    """
    return database.execute_query(query, (course_id,))

def report_student_courses(student_id):
    """Demonstrates JOIN between enrollments, courses, and instructors."""
    query = """
        SELECT c.course_code, c.course_name, i.name AS instructor, e.status, e.grade
        FROM enrollments e
        INNER JOIN courses c ON e.course_id = c.course_id
        LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
        WHERE e.student_id = ?
    """
    return database.execute_query(query, (student_id,))

def report_enrollment_counts():
    """Demonstrates GROUP BY and COUNT."""
    query = """
        SELECT c.course_code, c.course_name, COUNT(e.student_id) AS enrolled_count
        FROM courses c
        LEFT JOIN enrollments e ON c.course_id = e.course_id
        GROUP BY c.course_id
    """
    return database.execute_query(query)
