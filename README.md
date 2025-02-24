# FMS Abuja Payroll System

Welcome to the **FMS Abuja Payroll System**, a web application designed to streamline payroll management for administrators and employees. Built using **Flask**, **Bootstrap**, and **HTMX**, this system allows administrators to create users, generate payslips, and upload them for employees. Employees can then view and download their payslips securely.

## Features

- **Admin Features**:
  - Create and manage users with IPPIS numbers.
  - Generate and upload payslips for employees (both bulk and single uploads).
  - Manage payroll data efficiently.

- **Employee Features**:
  - View and download payslips.
  - Access payroll history securely.

## Technologies Used

- **Flask**: A lightweight Python web framework for building the backend.
- **Bootstrap**: A front-end framework for responsive and modern UI design.
- **HTMX**: A library for adding dynamic behavior to HTML without writing JavaScript.

## Installation

To get started with the FMS Abuja Payroll System, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/emperorsixpacks/fmsabujapayroll.git
   cd fmsabujapayroll
   ```

2. **Set Up a Virtual Environment**:
   Install `uv` (a modern Python package installer) if you don't already have it:
   ```bash
   pip install uv
   ```
   Create and activate the virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   Install the dependencies listed in the `pyproject.toml` file:
   ```bash
   uv pip install .
   #OR 
   uv pip install -r pyproject.toml
   ```

4. **Run Database Migrations**:
   Ensure the database is set up properly:
   ```bash
   python manage.py migrate
   ```

5. **Run the Application**:
   Use the provided script to run the app:
   ```bash
   python manage.py run
   ```
   To run in debug mode:
   ```bash
   python manage.py run debug
   ```

6. **Create an Admin User**:
   Run the `create_admin.py` script to create an admin account:
   ```bash
   python manage.py create_admin
   ```
   The script will prompt for email, first name, last name, password, and IPPIS number.

7. **Access the Application**:
   Open your browser and navigate to `http://localhost:5000` to access the payroll system.

## Usage

- **Admin Login**:
  - Log in with your admin credentials to create users, generate payslips (single and bulk uploads), and manage payroll data.

- **Employee Login**:
  - Employees can log in to view and download their payslips.

## Command-Line Interface (CLI)

- **Migrate Database**:
  ```bash
  python manage.py migrate
  ```
- **Run the Application**:
  ```bash
  python manage.py run
  ```
- **Run in Debug Mode**:
  ```bash
  python manage.py run debug
  ```
- **Create Admin User**:
  ```bash
  python manage.py create_admin
  ```


