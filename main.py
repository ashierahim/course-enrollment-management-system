import getpass
import sqlite3
import auth
import database
import students
import instructors
import courses
import enrollments
import reports
from utils import clear_screen, print_header, pause, get_valid_string, get_valid_integer, get_valid_email, get_menu_choice

def display_records(records, title="Records"):
    print_header(title)
    if not records:
        print("No records found.")
    else:
        for r in records:
            print(dict(r))
    pause()

def manage_users_menu():
    if not auth.require_role(['ADMIN']):
        print("Unauthorized access.")
        return
        
    while True:
        clear_screen()
        print_header("Manage Users (Admin Only)")
        print("1. View All Users")
        print("2. Update User Role")
        print("3. Delete User")
        print("4. Back")
        
        choice = get_menu_choice("Select an option: ", ['1', '2', '3', '4'])
        
        if choice == '1':
            display_records(auth.get_all_users(), "All Users")
        elif choice == '2':
            user_id = get_valid_integer("Enter User ID to update: ")
            role = get_menu_choice("Select new role (ADMIN/STAFF/STUDENT): ", ['ADMIN', 'STAFF', 'STUDENT'])
            success, msg = auth.update_user_role(user_id, role)
            print(msg)
            pause()
        elif choice == '3':
            user_id = get_valid_integer("Enter User ID to delete: ")
            success, msg = auth.delete_user(user_id)
            print(msg)
            pause()
        elif choice == '4':
            break

def manage_students_menu():
    if not auth.require_role(['ADMIN', 'STAFF']):
        print("Unauthorized access.")
        return
        
    while True:
        clear_screen()
        print_header("Manage Students")
        print("1. Add Student")
        print("2. View All Students")
        print("3. View Student by ID")
        print("4. Update Student")
        if auth.require_role(['ADMIN']):
            print("5. Delete Student (Admin Only)")
        print("6. Back")
        
        valid_choices = ['1', '2', '3', '4', '6']
        if auth.require_role(['ADMIN']):
            valid_choices.append('5')
            
        choice = get_menu_choice("Select an option: ", valid_choices)
        
        if choice == '1':
            user_id = get_valid_integer("Enter associated User ID: ")
            name = get_valid_string("Enter Name: ")
            email = get_valid_email("Enter Email: ")
            phone = get_valid_string("Enter Phone (optional): ", required=False)
            dept = get_valid_string("Enter Department: ")
            year = get_valid_integer("Enter Year (e.g., 1, 2, 3): ")
            success, msg = students.create_student(user_id, name, email, phone, dept, year)
            print(f"Result: {msg}")
            pause()
        elif choice == '2':
            display_records(students.get_all_students(), "All Students")
        elif choice == '3':
            student_id = get_valid_integer("Enter Student ID: ")
            student = students.get_student_by_id(student_id)
            display_records([student] if student else [], f"Student {student_id}")
        elif choice == '4':
            student_id = get_valid_integer("Enter Student ID to update: ")
            if students.get_student_by_id(student_id):
                name = get_valid_string("Enter Name: ")
                email = get_valid_email("Enter Email: ")
                phone = get_valid_string("Enter Phone (optional): ", required=False)
                dept = get_valid_string("Enter Department: ")
                year = get_valid_integer("Enter Year: ")
                success, msg = students.update_student(student_id, name, email, phone, dept, year)
                print(msg)
            else:
                print("Student not found.")
            pause()
        elif choice == '5':
            student_id = get_valid_integer("Enter Student ID to delete: ")
            success, msg = students.delete_student(student_id)
            print(msg)
            pause()
        elif choice == '6':
            break

def manage_instructors_menu():
    if not auth.require_role(['ADMIN', 'STAFF']):
        print("Unauthorized access.")
        return
        
    while True:
        clear_screen()
        print_header("Manage Instructors")
        print("1. View All Instructors")
        print("2. View Instructor by ID")
        if auth.require_role(['ADMIN']):
            print("3. Add Instructor")
            print("4. Update Instructor")
            print("5. Delete Instructor")
        print("6. Back")
        
        valid_choices = ['1', '2', '6']
        if auth.require_role(['ADMIN']):
            valid_choices.extend(['3', '4', '5'])
            
        choice = get_menu_choice("Select an option: ", valid_choices)
        
        if choice == '1':
            display_records(instructors.get_all_instructors(), "All Instructors")
        elif choice == '2':
            instructor_id = get_valid_integer("Enter Instructor ID: ")
            instructor = instructors.get_instructor_by_id(instructor_id)
            display_records([instructor] if instructor else [], f"Instructor {instructor_id}")
        elif choice == '3':
            user_id = get_valid_integer("Enter associated User ID: ")
            name = get_valid_string("Enter Name: ")
            email = get_valid_email("Enter Email: ")
            dept = get_valid_string("Enter Department: ")
            success, msg = instructors.create_instructor(user_id, name, email, dept)
            print(f"Result: {msg}")
            pause()
        elif choice == '4':
            instructor_id = get_valid_integer("Enter Instructor ID to update: ")
            if instructors.get_instructor_by_id(instructor_id):
                name = get_valid_string("Enter Name: ")
                email = get_valid_email("Enter Email: ")
                dept = get_valid_string("Enter Department: ")
                success, msg = instructors.update_instructor(instructor_id, name, email, dept)
                print(msg)
            else:
                print("Instructor not found.")
            pause()
        elif choice == '5':
            instructor_id = get_valid_integer("Enter Instructor ID to delete: ")
            success, msg = instructors.delete_instructor(instructor_id)
            print(msg)
            pause()
        elif choice == '6':
            break

def manage_courses_menu():
    if not auth.require_role(['ADMIN', 'STAFF']):
        print("Unauthorized access.")
        return
        
    while True:
        clear_screen()
        print_header("Manage Courses")
        print("1. Add Course")
        print("2. View All Courses")
        print("3. Update Course")
        if auth.require_role(['ADMIN']):
            print("4. Delete Course")
        print("5. Back")
        
        valid_choices = ['1', '2', '3', '5']
        if auth.require_role(['ADMIN']):
            valid_choices.append('4')
            
        choice = get_menu_choice("Select an option: ", valid_choices)
        
        if choice == '1':
            code = get_valid_string("Enter Course Code: ")
            name = get_valid_string("Enter Course Name: ")
            desc = get_valid_string("Enter Description (optional): ", required=False)
            credits = get_valid_integer("Enter Credits: ", min_value=0)
            inst_id = get_valid_integer("Enter Instructor ID (optional): ", required=False)
            success, msg = courses.create_course(code, name, desc, credits, inst_id)
            print(f"Result: {msg}")
            pause()
        elif choice == '2':
            display_records(courses.get_all_courses(), "All Courses")
        elif choice == '3':
            course_id = get_valid_integer("Enter Course ID to update: ")
            if courses.get_course_by_id(course_id):
                code = get_valid_string("Enter Course Code: ")
                name = get_valid_string("Enter Course Name: ")
                desc = get_valid_string("Enter Description (optional): ", required=False)
                credits = get_valid_integer("Enter Credits: ", min_value=0)
                inst_id = get_valid_integer("Enter Instructor ID (optional): ", required=False)
                success, msg = courses.update_course(course_id, code, name, desc, credits, inst_id)
                print(msg)
            else:
                print("Course not found.")
            pause()
        elif choice == '4':
            course_id = get_valid_integer("Enter Course ID to delete: ")
            success, msg = courses.delete_course(course_id)
            print(msg)
            pause()
        elif choice == '5':
            break

def manage_enrollments_menu():
    if not auth.require_role(['ADMIN', 'STAFF']):
        print("Unauthorized access.")
        return
        
    while True:
        clear_screen()
        print_header("Manage Enrollments")
        print("1. Create Enrollment")
        print("2. View All Enrollments")
        print("3. Update Enrollment Status/Grade")
        if auth.require_role(['ADMIN']):
            print("4. Delete Enrollment")
        print("5. Back")
        
        valid_choices = ['1', '2', '3', '5']
        if auth.require_role(['ADMIN']):
            valid_choices.append('4')
            
        choice = get_menu_choice("Select an option: ", valid_choices)
        
        if choice == '1':
            student_id = get_valid_integer("Enter Student ID: ")
            course_id = get_valid_integer("Enter Course ID: ")
            success, msg = enrollments.enroll_student(student_id, course_id)
            print(f"Result: {msg}")
            pause()
        elif choice == '2':
            display_records(enrollments.get_all_enrollments(), "All Enrollments")
        elif choice == '3':
            enrollment_id = get_valid_integer("Enter Enrollment ID to update: ")
            status = get_menu_choice("Enter Status (ENROLLED, DROPPED, COMPLETED): ", ['ENROLLED', 'DROPPED', 'COMPLETED'])
            grade = get_valid_string("Enter Grade (e.g., A, B, C) or leave empty: ", required=False)
            success, msg = enrollments.update_enrollment_status_grade(enrollment_id, status, grade)
            print(msg)
            pause()
        elif choice == '4':
            enrollment_id = get_valid_integer("Enter Enrollment ID to delete: ")
            success, msg = enrollments.delete_enrollment(enrollment_id)
            print(msg)
            pause()
        elif choice == '5':
            break

def reports_menu():
    if not auth.require_role(['ADMIN', 'STAFF']):
        print("Unauthorized access.")
        return
        
    while True:
        clear_screen()
        print_header("Reports Dashboard")
        print("1. Courses with Instructors")
        print("2. Students in a Course")
        print("3. Enrollment Counts per Course")
        print("4. Back")
        
        choice = get_menu_choice("Select an option: ", ['1', '2', '3', '4'])
        
        if choice == '1':
            display_records(reports.report_courses_with_instructors(), "Courses & Instructors")
        elif choice == '2':
            course_id = get_valid_integer("Enter Course ID: ")
            display_records(reports.report_students_in_course(course_id), f"Students in Course {course_id}")
        elif choice == '3':
            display_records(reports.report_enrollment_counts(), "Enrollment Counts")
        elif choice == '4':
            break

def admin_dashboard():
    while True:
        clear_screen()
        print_header("ADMIN DASHBOARD")
        print("1. Manage Users")
        print("2. Manage Students")
        print("3. Manage Instructors")
        print("4. Manage Courses")
        print("5. Manage Enrollments")
        print("6. Reports")
        print("7. Logout")
        
        choice = get_menu_choice("Select an option: ", [str(i) for i in range(1, 8)])
        
        if choice == '1': manage_users_menu()
        elif choice == '2': manage_students_menu()
        elif choice == '3': manage_instructors_menu()
        elif choice == '4': manage_courses_menu()
        elif choice == '5': manage_enrollments_menu()
        elif choice == '6': reports_menu()
        elif choice == '7':
            auth.logout()
            break

def staff_dashboard():
    while True:
        clear_screen()
        print_header("STAFF DASHBOARD")
        print("1. Manage Students")
        print("2. View Instructors")
        print("3. Manage Courses")
        print("4. Manage Enrollments")
        print("5. Reports")
        print("6. Logout")
        
        choice = get_menu_choice("Select an option: ", [str(i) for i in range(1, 7)])
        
        if choice == '1': manage_students_menu()
        elif choice == '2': manage_instructors_menu()
        elif choice == '3': manage_courses_menu()
        elif choice == '4': manage_enrollments_menu()
        elif choice == '5': reports_menu()
        elif choice == '6':
            auth.logout()
            break

def student_dashboard():
    while True:
        clear_screen()
        print_header("STUDENT DASHBOARD")
        
        user = auth.get_current_user()
        student_record = students.get_student_by_user_id(user['id'])
        
        if not student_record:
            print("Your student profile has not been created yet.")
            print("Please contact an administrator.")
            print("\n1. Logout")
            get_menu_choice("Select an option: ", ['1'])
            auth.logout()
            break
            
        student_id = student_record['student_id']
        
        print("1. View My Profile")
        print("2. Update My Profile (Phone/Dept/Year)")
        print("3. View Available Courses")
        print("4. Enroll in Course")
        print("5. View My Enrollments & Grades")
        print("6. Logout")
        
        choice = get_menu_choice("Select an option: ", [str(i) for i in range(1, 7)])
        
        if choice == '1':
            display_records([student_record], "My Profile")
        elif choice == '2':
            phone = get_valid_string(f"Enter Phone [{student_record['phone']}]: ", required=False) or student_record['phone']
            dept = get_valid_string(f"Enter Department [{student_record['department']}]: ", required=False) or student_record['department']
            year = get_valid_integer(f"Enter Year [{student_record['year']}]: ", required=False) or student_record['year']
            
            success, msg = students.update_student(student_id, student_record['name'], student_record['email'], phone, dept, year)
            print(msg)
            pause()
        elif choice == '3':
            display_records(courses.get_all_courses(), "Available Courses")
        elif choice == '4':
            course_id = get_valid_integer("Enter Course ID to enroll in: ")
            success, msg = enrollments.enroll_student(student_id, course_id)
            print(msg)
            pause()
        elif choice == '5':
            display_records(reports.report_student_courses(student_id), "My Enrollments")
        elif choice == '6':
            auth.logout()
            break

def setup_sample_data():
    """Inserts default users for testing if the database is fresh."""
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()['count']
    conn.close()
    
    if count == 0:
        print("Creating sample data...")
        auth.register_user('admin', 'admin123', 'ADMIN')
        auth.register_user('staff', 'staff123', 'STAFF')

def main_menu():
    while True:
        clear_screen()
        print_header("COURSE ENROLLMENT MANAGEMENT SYSTEM")
        print("1. Login")
        print("2. Register (Student Only)")
        print("3. Exit")
        
        choice = get_menu_choice("Select an option: ", ['1', '2', '3'])
        
        if choice == '1':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            
            success, user_or_msg = auth.login(username, password)
            if success:
                user = auth.get_current_user()
                if user['role'] == 'ADMIN':
                    admin_dashboard()
                elif user['role'] == 'STAFF':
                    staff_dashboard()
                elif user['role'] == 'STUDENT':
                    student_dashboard()
            else:
                print(user_or_msg)
                pause()
                
        elif choice == '2':
            print("\n--- Student Registration ---")
            username = input("Enter new username: ")
            password = getpass.getpass("Enter new password: ")
            
            success, msg = auth.register_user(username, password, 'STUDENT')
            if success:
                print("Registration successful! You can now login.")
                print("Note: An Admin or Staff must create your student profile before you can enroll in courses.")
            else:
                print(f"Registration failed: {msg}")
            pause()
            
        elif choice == '3':
            print("Exiting system. Goodbye!")
            break

def main():
    try:
        database.init_db()
        setup_sample_data()
        main_menu()
    except Exception as e:
        print(f"A critical error occurred: {e}")

if __name__ == "__main__":
    main()
