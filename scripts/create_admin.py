import sys

from werkzeug.security import generate_password_hash

from payroll.app import app
from payroll.models import User, db


def get_input(prompt):
    """Helper function to ensure input is not empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required. Please enter a value.")


def create_admin():
    """Creates an admin user if one doesn't exist."""
    with app.app_context():
        email = get_input("Enter admin email: ")
        first_name = get_input("Enter admin first name: ")
        last_name = get_input("Enter admin last name: ")
        ippis_number = get_input("Enter admin IPPIS number: ")
        password = get_input("Enter admin password: ")

        try:
            if User.query.filter_by(email=email).first():
                print("Admin user already exists!")
                sys.exit(1)

            admin = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                ippis_number=ippis_number,
                password_hash=generate_password_hash(password),
                role="admin",
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        except Exception as e:
            print(e)
