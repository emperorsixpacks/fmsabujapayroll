import sys
import subprocess
from waitress import serve
from payroll.app import app 

def run():
    if sys.platform == "win32":
        print("Running on Windows with Waitress...")
        serve(app, host='0.0.0.0', port=5000)
    else:
        print("Running on Linux with Gunicorn...")
        subprocess.run(["gunicorn", "payroll.app:app", "-b", "0.0.0.0:5000"])

if __name__ == "__main__":
    run()