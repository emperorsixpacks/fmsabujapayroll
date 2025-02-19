import os
from dotenv import load_dotenv
from payroll.app import app
from payroll.models import db

load_dotenv(".env")
DEBUG= bool(int(os.environ.get("DEBUG", 1)))
def run():
    with app.app_context():
        db.create_all()  # Ensure the database is created
    app.run(debug=DEBUG)


if __name__ == "__main__":
    run()
