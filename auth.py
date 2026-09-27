import hashlib
import getpass
import database
import sqlite3

# Simple in-memory session
current_user = None

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password, hashed_password):
    """Verifies a password against a hash."""
    return hash_password(password) == hashed_password

def register_user(username, password, role):
    """Registers a new user in the system."""
    try:
        hashed_pw = hash_password(password)
        query = "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"
        user_id = database.execute_query(query, (username, hashed_pw, role), commit=True)
        return True, user_id
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    except Exception as e:
        return False, str(e)

def login(username, password):
    """Authenticates a user and sets the current session."""
    global current_user
    query = "SELECT id, username, password_hash, role FROM users WHERE username = ?"
    user = database.execute_fetchone(query, (username,))
    
    if user and verify_password(password, user['password_hash']):
        current_user = {
            'id': user['id'],
            'username': user['username'],
            'role': user['role']
        }
        return True, current_user
    return False, "Invalid username or password."

def logout():
    """Clears the current session."""
    global current_user
    current_user = None

def get_current_user():
    """Returns the currently logged-in user."""
    return current_user

def require_role(allowed_roles):
    """Decorator or check for role-based authorization."""
    if not current_user:
        return False
    return current_user['role'] in allowed_roles

def get_all_users():
    return database.execute_query("SELECT id, username, role, created_at FROM users")

def get_user_by_id(user_id):
    return database.execute_fetchone("SELECT id, username, role, created_at FROM users WHERE id = ?", (user_id,))

def delete_user(user_id):
    try:
        database.execute_query("DELETE FROM users WHERE id = ?", (user_id,), commit=True)
        return True, "User deleted successfully."
    except Exception as e:
        return False, str(e)

def update_user_role(user_id, new_role):
    try:
        database.execute_query("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id), commit=True)
        return True, "User role updated successfully."
    except Exception as e:
        return False, str(e)
