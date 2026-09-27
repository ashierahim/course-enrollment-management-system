import os
import re

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Prints a formatted header."""
    print("\n" + "=" * 40)
    print(f" {title.upper()}")
    print("=" * 40 + "\n")

def pause():
    """Pauses execution until the user presses Enter."""
    input("\nPress Enter to continue...")

def get_valid_string(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if not value and required:
            print("Error: This field cannot be empty.")
            continue
        return value

def get_valid_integer(prompt, required=True, min_value=None):
    while True:
        value_str = input(prompt).strip()
        if not value_str:
            if required:
                print("Error: This field cannot be empty.")
                continue
            return None
        
        try:
            value = int(value_str)
            if min_value is not None and value < min_value:
                print(f"Error: Value must be at least {min_value}.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid integer.")

def get_valid_email(prompt, required=True):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    while True:
        email = get_valid_string(prompt, required)
        if not email and not required:
            return None
        if re.match(pattern, email):
            return email
        print("Error: Please enter a valid email address.")

def get_menu_choice(prompt, valid_choices):
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Error: Invalid choice. Please select from {', '.join(valid_choices)}.")
