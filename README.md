# TaskFlow – To-Do Web Application

## Overview

TaskFlow is a web-based application that helps users manage their daily tasks efficiently. It allows users to create, track, and complete tasks with a clean and modern interface, improving productivity and organization.

## Features

* User registration and login
* Add tasks with deadlines
* Mark tasks as completed
* Delete tasks
* Profile page to view user details
* Smooth navigation between dashboard and profile
* Responsive and modern UI

## Technologies Used

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python (Flask)

### Database

* MySQL

## How It Works

* Users register and log in to the system
* Users can add tasks along with deadlines
* Tasks are displayed on the dashboard
* Users can mark tasks as completed or delete them
* All data is stored and retrieved from a MySQL database

## Database Tables

* Users: stores user credentials
* Tasks: stores user tasks, deadlines, and status

## How to Run

### 1. Install Dependencies

```bash
pip install flask mysql-connector-python
```

### 2. Setup Database

```sql
CREATE DATABASE todo_app;

USE todo_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    task TEXT,
    deadline DATE,
    status INT DEFAULT 0
);
```

### 3. Configure Database

Update your database password in `app.py`:

```python
password="YOUR_PASSWORD"
```

### 4. Run the Application

```bash
python app.py
```

### 5. Access the Application

Open your browser and go to:
http://127.0.0.1:5000/login

## Future Improvements

* Password encryption (bcrypt)
* Task categories and priorities
* Notifications and reminders
* Data visualization (task analytics)
* Deployment to cloud platforms

## Conclusion

TaskFlow is a simple yet effective task management application built using Flask and MySQL. It demonstrates core web development concepts including authentication, database integration, and interactive UI design.
