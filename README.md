# Employee-Management-System

## Introduction

Hello Everyone, Myself Aritra Shee. I developed a new "Employee Management System". The system has a powerful authenticated login feature with a secure hashing password generator in the DB and a very easy & simple UI or interface. The Employee Management System is a comprehensive web-based application designed to streamline HR processes and enhance the management of employee data within organizations. Developed using Flask, a lightweight yet powerful Python web framework, this system integrates robust tools such as SQLAlchemy for seamless interaction with a MySQL database managed through phpMyAdmin, Flask-Login for secure user authentication, and Flask-WTF for secure form handling.

## Features

- **User Registration and Login**: A secure interface for HR users to register and log in, ensuring that only authorized personnel have access to sensitive employee data.
- **Employee Record Management**: Functionality for HR professionals to add, update, and manage comprehensive employee records, including personal details, employment history, and organizational roles.
- **Data Integrity and Security**: Robust security measures and validation rules to maintain data accuracy and integrity, protecting sensitive information from unauthorized access.

## Requirements

1. IDE: MS VS Code or Jetbrains PyCharm
2. Scripting or Programming Language for Backend Development: Python Latest Version
3. Modules:
   - Flask
   - Flask-SQLAlchemy
   - Flask-Login
   - Flask-Bcrypt
   - Flask-WTF
4. For making DB: XAMPP Control Panel/Direct Query in MySQL LocalHost or SQLite3 LocalHost & DB Instance. I used XAMPP for first working.

## Installation

1. **VS Code**: [Installation Guide](https://youtu.be/bN6DE-4uFNo?si=4R80cx2pFUBmiG7a)
2. **PyCharm**: [Installation Guide](https://youtu.be/6a2cSXgooDo?si=3CTOyto1Z2-xjEW7)
3. **Python**: Follow the installation guides above.
4. **Flask & Its Sub-modules**:
    ```bash
    pip install flask flask-sqlalchemy flask-login flask-bcrypt flask-wtf
    ```

## Database Setup

1. Open XAMPP Control Panel and start Apache and MySQL.
2. Click on MySQL Admin to open phpMyAdmin.
3. Create a new database and run the following SQL queries:

    ```sql
    CREATE TABLE employee (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        phone VARCHAR(15) NOT NULL UNIQUE,
        address VARCHAR(255) NOT NULL,
        joining_date DATE NOT NULL,
        designation VARCHAR(100) NOT NULL,
        organization_id INT,
        FOREIGN KEY (organization_id) REFERENCES organization(id)
    );

    CREATE TABLE organization (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL
    );

    CREATE TABLE user (
        id INT PRIMARY KEY AUTO_INCREMENT,
        first_name VARCHAR(70) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(60) NOT NULL,
        organization VARCHAR(100) NOT NULL,
        organization_id INT,
        FOREIGN KEY (organization_id) REFERENCES organization(id)
    );
    ```

## Virtual Environment Setup

It is recommended to use a virtual environment to manage dependencies. This ensures that the installed packages do not interfere with other projects.

1. **Create a Virtual Environment**:
    ```bash
    python -m venv venv

    or

    select venv during project folder creation
    ```

### Troubleshooting Virtual Environment Activation

First, we create a Python project & while creating, we have to select `venv` as the interpreter. After this process, sometimes `venv` does not show in the project directory, or sometimes it is not activated, resulting in module errors. Follow these steps to resolve such issues:

#### If `venv` shows but is not activated:

1. **Activate the Virtual Environment**:
   - On **Windows**:
        ```bash
        venv\Scripts\activate
        ```
   - On **macOS and Linux**:
        ```bash
        source venv/bin/activate
        ```

2. **Using VS Code or PyCharm Terminal**:
   - **VS Code**: Open the integrated terminal and run the appropriate command based on your operating system.
   - **PyCharm**: Open the terminal within PyCharm and run the appropriate command.

#### If `venv` was selected but does not show in the project directory:

1. **Recreate the Virtual Environment**:
    ```bash
    python -m venv venv
    ```

2. **Activate the Virtual Environment**:
   - On **Windows**:
        ```bash
        venv\Scripts\activate
        ```
   - On **macOS and Linux**:
        ```bash
        source venv/bin/activate
        ```

#### After activating the virtual environment:

3. **Install Required Packages**:
    ```bash
    pip install flask flask-sqlalchemy flask-login flask-bcrypt flask-wtf
    ```

4. **Deactivating the Virtual Environment**:
    ```bash
    deactivate
    ```

## Usage

1. **Run the Flask Application**:
    ```bash
    python app.py
    ```

2. **Access the Application**:
    Open your web browser and go to `http://localhost:5000`.

    If you need to run the application on a different port, you can specify the port number like this:
    ```bash
    python app.py -p 8080
    ```
    Then access the application at `http://localhost:8080`.
    Note: Every Backend (Framework & Non Framework both) in Python & any other language (Scripting or Programming) has differnt port number, such as Python Flask's port number is always 5000.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions, suggestions, or feedback, please contact me at:

- **Name**: Aritra Shee
- **Email**: [gameraritra5@gmail.com](mailto:gameraritra5@gmail.com)
- **LinkedIn**: [Aritra Shee](https://www.linkedin.com/in/aritra-shee-58393723a)