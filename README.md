# Employee Management System

A beginner-friendly **3-Tier Architecture** project built using **Python**, **Flask**, **HTML/CSS/JavaScript**, and **PostgreSQL (Docker)**.

This project demonstrates how a real Python backend application is structured using REST APIs and a relational database.

---

## 📌 Project Overview

The application allows users to:

- Add Employee
- View Employees
- Update Employee
- Delete Employee

This project follows the **3-Tier Architecture**.

```
Presentation Layer
        │
        ▼
Business Layer (Flask REST API)
        │
        ▼
Database Layer (PostgreSQL)
```

---

# 🏗 Architecture

```
                    Browser

                        │

        HTML + CSS + JavaScript

                        │

                HTTP REST API

                        │

                 Flask Application

                        │

                  SQLAlchemy ORM

                        │

                  PostgreSQL Docker
```

---

# 🛠 Tech Stack

| Technology | Version |
|------------|---------|
| Python | 3.12+ |
| Flask | Latest |
| PostgreSQL | 17 |
| SQLAlchemy | Latest |
| Docker | Latest |
| HTML5 | Latest |
| CSS3 | Latest |
| JavaScript | ES6 |

---

# 📁 Project Structure

```
employee-management/

│

├── backend/

│   ├── app.py

│   ├── config.py

│   ├── database.py

│   ├── models.py

│   ├── routes.py

│   ├── services.py

│   ├── repository.py

│   ├── requirements.txt

│

├── frontend/

│   ├── index.html

│   ├── style.css

│   ├── script.js

│

├── database/

│   ├── init.sql

│

├── docker-compose.yml

│

└── README.md
```

---

# Features

- CRUD Operations
- REST API
- PostgreSQL Database
- Docker Support
- Responsive UI
- JSON API
- Input Validation
- Clean Folder Structure

---

# Prerequisites

Install the following software:

- Python 3.12+
- Docker Desktop
- Git
- Visual Studio Code

---

# Clone Project

```bash
git clone https://github.com/yourusername/employee-management.git

cd employee-management
```

---

# Start PostgreSQL Using Docker

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

---

# Database Configuration

Default Configuration

```
Host        : localhost

Port        : 5432

Database    : EmployeeDB

Username    : admin

Password    : Password@123
```

---

# Install Python Packages

```bash
pip install -r backend/requirements.txt
```

---

# Run Backend

```bash
cd backend

python app.py
```

Application starts on

```
http://localhost:5000
```

---

# Open Frontend

Open

```
frontend/index.html
```

---

# REST APIs

## Get Employees

```
GET /employees
```

---

## Add Employee

```
POST /employees
```

Example

```json
{
    "name":"John",
    "email":"john@test.com",
    "department":"IT",
    "salary":50000
}
```

---

## Update Employee

```
PUT /employees/1
```

---

## Delete Employee

```
DELETE /employees/1
```

---

# Database Table

```
Employees
-------------------------

Id

Name

Email

Department

Salary
```

---

# Development Flow

```
Frontend

↓

JavaScript Fetch

↓

Flask REST API

↓

Business Logic

↓

SQLAlchemy

↓

PostgreSQL

↓

JSON Response

↓

Frontend
```

---

# Future Enhancements

- Login
- JWT Authentication
- Role Based Authorization
- Search
- Pagination
- Sorting
- Dockerize Flask
- Docker Compose
- Unit Testing
- Logging
- Redis Cache
- Swagger Documentation
- CI/CD Pipeline
- Azure Deployment

---

# Learning Objectives

By completing this project you will learn

- Python Basics
- Flask REST API
- SQLAlchemy ORM
- PostgreSQL
- Docker
- CRUD Operations
- HTTP Methods
- JSON
- REST Architecture
- Three Tier Architecture
- Database Design

---

# Screenshots

Add screenshots here.

```
Home Page

Employee List

Add Employee

Edit Employee
```

---

# Author

Nagendra Babu

Python Developer Learning Project

---

# License

MIT License
