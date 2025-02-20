
# FMS Abuja Payroll System

Welcome to the **FMS Abuja Payroll System**, a web application designed to streamline payroll management for administrators and employees. Built using **Flask**, **Bootstrap**, and **HTMX**, this system allows administrators to create users, generate payslips, and upload them for employees. Employees can then view and download their payslips securely.

## Features

- **Admin Features**:
  - Create and manage users.
  - Generate and upload payslips for employees.
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
   ```

4. **Run the Application**:
   Use the provided script to run the app:
   ```bash
   python -m run
   ```

5. **Create an Admin User**:
   Run the `create_admin.py` script to create an admin account:
   ```bash
   python -m scripts.create_admin
   ```

6. **Access the Application**:
   Open your browser and navigate to `http://localhost:5000` to access the payroll system.

## Usage

- **Admin Login**:
  - Log in with your admin credentials to create users, generate payslips, and manage payroll data.

- **Employee Login**:
  - Employees can log in to view and download their payslips.
