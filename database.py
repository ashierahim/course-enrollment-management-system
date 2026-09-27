import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'course_enrollment.db')

def get_connection():
    """Returns a connection to the SQLite database with foreign keys enabled."""
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
        
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    # Return rows as dictionaries to make data access easier
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('ADMIN', 'STAFF', 'STUDENT')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Students Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            department TEXT,
            year INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # 3. Instructors Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # 4. Courses Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT UNIQUE NOT NULL,
            course_name TEXT NOT NULL,
            description TEXT,
            credits INTEGER NOT NULL CHECK(credits >= 0),
            instructor_id INTEGER,
            FOREIGN KEY(instructor_id) REFERENCES instructors(instructor_id) ON DELETE SET NULL
        )
    ''')
    
    # 5. Enrollments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'ENROLLED',
            grade TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
            UNIQUE(student_id, course_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def execute_query(query, params=(), commit=False):
    """Executes a single query and returns the results or handles commit."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if commit:
            conn.commit()
            return cursor.lastrowid
        else:
            return cursor.fetchall()
    except sqlite3.Error as e:
        if commit:
            conn.rollback()
        raise e
    finally:
        conn.close()

def execute_fetchone(query, params=()):
    """Executes a query and returns a single row."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    finally:
        conn.close()
