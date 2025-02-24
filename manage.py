import sys
import subprocess
import argparse
from waitress import serve
from payroll.app import app
from payroll.models import db  # Ensure this imports your database instance
from scripts.create_admin import create_admin

def migrate():
    """Handles database migration (creates tables)."""
    with app.app_context():
        db.create_all()
        print("✅ Database migrated successfully.")

def run():
    """Runs the app with either Waitress (Windows) or Gunicorn (Linux)."""
    if sys.platform == "win32":
        print("🚀 Running on Windows with Waitress...")
        serve(app, host='0.0.0.0', port=5000)
    else:
        print("🚀 Running on Linux with Gunicorn...")
        subprocess.run(["gunicorn", "payroll.app:app", "-b", "0.0.0.0:5000"])

def run_debug():
    """Runs the app in debug mode."""
    print("🚀 Running in Debug mode...")
    app.run(debug=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage the payroll system.")
    parser.add_argument("command", choices=["migrate", "run", "run-debug", "create-admin"], help="Command to execute")

    args = parser.parse_args()

    if args.command == "migrate":
        migrate()
    elif args.command == "run":
        run()
    elif args.command == "run-debug":
        run_debug()
    elif args.command == "create-admin":
        create_admin()
