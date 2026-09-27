# Course Enrollment Management System

## Objective
A complete Command-Line Interface (CLI) based Database Management System project demonstrating relational database concepts, CRUD operations, authentication, and role-based access control.

## Features
- **Authentication:** Registration, login, and secure password hashing (SHA-256).
- **Roles:** Three user roles (ADMIN, STAFF, STUDENT) with distinct permissions.
- **CRUD Operations:** Complete Create, Read, Update, and Delete operations for Users, Students, Instructors, Courses, and Enrollments.
- **Relational Database:** SQLite with foreign keys, cascading deletes, and unique constraints.
- **Reporting:** Uses SQL JOIN queries to generate multi-table reports.
- **Validation & Exception Handling:** Robust error handling preventing application crashes on invalid input or database errors.

## Technologies
- **Python 3.x**
- **SQLite3** (Standard Library)
- **Hashlib** (Standard Library)

## Project Structure
```text
course_enrollment_system/
├── main.py             # Entry point, login, and registration logic
├── database.py         # DB connection and schema initialization
├── config.py           # Configuration variables
├── auth.py             # Authentication and session management
├── users.py            # User operations
├── students.py         # Student CRUD
├── instructors.py      # Instructor CRUD
├── courses.py          # Course CRUD
├── enrollments.py      # Enrollment CRUD
├── reports.py          # JOIN queries for reporting
├── menus.py            # Role-based interactive menus
├── validators.py       # Input validation handlers
├── utils.py            # CLI helpers
├── database/           # SQLite database directory
│   └── course_enrollment.db
├── tests/              # Unittest suite
│   └── test_system.py
├── README.md           # Documentation
└── requirements.txt    # Empty (standard library only)
```

## Database Schema & Table Relationships
The system uses 5 related tables:
1. `users` (id, username, password_hash, role)
2. `students` (student_id, user_id, name, email, phone, department, year)
3. `instructors` (instructor_id, user_id, name, email, department)
4. `courses` (course_id, course_code, course_name, description, credits, instructor_id)
5. `enrollments` (enrollment_id, student_id, course_id, status, grade)

**Relationships:**
- `students.user_id` -> `users.id` (1:1)
- `instructors.user_id` -> `users.id` (1:1)
- `courses.instructor_id` -> `instructors.instructor_id` (N:1)
- `enrollments.student_id` -> `students.student_id` (N:1)
- `enrollments.course_id` -> `courses.course_id` (N:1)

## Setup and Execution
No external dependencies are required. Just ensure Python 3 is installed.

```bash
# Clone/download the directory, then navigate into it
cd course_enrollment_system

# Run the application
python main.py
```
*The SQLite database will be created automatically upon the first run.*

## Sample Login Credentials
The system automatically creates these accounts on the first run if the database is empty:

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Staff Account:**
- Username: `staff`
- Password: `staff123`

## Running Tests
A comprehensive test suite is included to verify CRUD, database constraints, and application logic.
```bash
python -m unittest discover -s tests
```
