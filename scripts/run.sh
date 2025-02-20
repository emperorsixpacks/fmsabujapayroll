#!/bin/bash

echo "Starting Payroll Flask App..."

# Activate Virtual Environment (Modify this path based on your cPanel setup)
source .venv/bin/activate  # Adjust Python version

# Navigate to the project directory

# Run the app using Waitress
gunicorn --bind 0.0.0.0:5000 main:app
