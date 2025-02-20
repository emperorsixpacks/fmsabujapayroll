import sys
from payroll.models import db, User
from payroll.app import app
from werkzeug.security import generate_password_hash


def create_admin():
    """Creates an admin user if one doesn't exist."""
    with app.app_context():
        email = input("Enter admin email: ")
        first_name = input("Enter admin first name: ")
        last_name = input("Enter admin last name: ")
        password = input("Enter admin password: ")

        if User.query.filter_by(email=email).first():
            print("Admin user already exists!")
            sys.exit(1)
        
        admin = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=generate_password_hash(password),
            role="admin",
        )

        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")


if __name__ == "__main__":
    create_admin()
