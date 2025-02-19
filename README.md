
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
   Install `uv` (a Python virtual environment tool) if you don't already have it:
   ```bash
   pip install uv
   ```
   Create and activate the virtual environment:
   ```bash
   uv venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   Use the provided script to run the app:
   ```bash
   ./scripts/run
   ```

5. **Create an Admin User**:
   Run the `create_admin.py` script to create an admin account:
   ```bash
   python ./scripts/create_admin.py
   ```

6. **Access the Application**:
   Open your browser and navigate to `http://localhost:5000` to access the payroll system.

## Usage

- **Admin Login**:
  - Log in with your admin credentials to create users, generate payslips, and manage payroll data.

- **Employee Login**:
  - Employees can log in to view and download their payslips.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your fork.
4. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask: https://flask.palletsprojects.com/
- Bootstrap: https://getbootstrap.com/
- HTMX: https://htmx.org/
```

This `README.md` provides a clear overview of the project, installation instructions, and usage details. Let me know if you need further adjustments!
