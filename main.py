from payroll.app import app
from payroll.models import db


def run():
    with app.app_context():
        db.create_all()  # Ensure the database is created
    app.run(debug=True)


if __name__ == "__main__":
    run()
