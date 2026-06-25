# Local Testing Guide — Employee Management System

This guide is for freshers who want to run and test this project on their own laptop from scratch.

---

## What You Will Need

Download and install these before starting:

| Tool | Download Link | Why |
|---|---|---|
| Python 3.12+ | https://www.python.org/downloads/ | Runs the Flask backend |
| Docker Desktop | https://www.docker.com/products/docker-desktop/ | Runs SQL Server database |
| Git | https://git-scm.com/downloads | Downloads the project |
| VS Code | https://code.visualstudio.com/ | To view and edit code |

---

## Step 1 — Download the Project

Open a terminal (Command Prompt on Windows, Terminal on Mac) and run:

```bash
git clone https://github.com/nagendraclouddevops/Employee-Management-System.git
```

Then go into the project folder:

```bash
cd Employee-Management-System
```

---

## Step 2 — Start SQL Server Using Docker

Make sure Docker Desktop is open and running first.

Then run this command to start a SQL Server container:

```bash
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=YourStrong@Passw0rd" \
  -p 1433:1433 --name sqlserver \
  -d mcr.microsoft.com/mssql/server:2022-latest
```

**What this does:**
- Downloads SQL Server 2022 from Docker
- Starts it on port 1433
- Sets the password to `YourStrong@Passw0rd`

Verify it is running:

```bash
docker ps
```

You should see a container named `sqlserver` with status `Up`.

---

## Step 3 — Create the Database and Tables

Run these two commands one by one:

**Create the database:**

```bash
docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'YourStrong@Passw0rd' -No \
  -Q "CREATE DATABASE EmployeeDB;"
```

**Create the tables:**

```bash
docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'YourStrong@Passw0rd' -No \
  -d EmployeeDB -Q "
CREATE TABLE Employees (
    Id INT IDENTITY PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Department VARCHAR(100),
    Salary DECIMAL(10,2)
);
CREATE TABLE Users (
    Id INT IDENTITY PRIMARY KEY,
    Username VARCHAR(100) UNIQUE NOT NULL,
    PasswordHash VARCHAR(256) NOT NULL
);"
```

---

## Step 4 — Create a Login User

To log in to the app you need a user in the database. Run this Python command to create one:

```bash
python3 -c "
from werkzeug.security import generate_password_hash
print(generate_password_hash('admin123'))
"
```

Copy the output (it will be a long hash string starting with `scrypt:...`).

Then run this command — replace `PASTE_HASH_HERE` with the copied hash:

```bash
docker exec sqlserver /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U SA -P 'YourStrong@Passw0rd' -No \
  -d EmployeeDB \
  -Q "INSERT INTO Users (Username, PasswordHash) VALUES ('admin', 'PASTE_HASH_HERE');"
```

Your login credentials will be:
```
Username: admin
Password: admin123
```

---

## Step 5 — Install Python Packages

```bash
pip install flask pymssql flask-cors
```

This installs:
- **flask** — the web framework for the backend
- **pymssql** — connects Python to SQL Server
- **flask-cors** — allows the frontend to talk to the backend

---

## Step 6 — Start the Backend (Flask)

Open a new terminal window and run:

```bash
cd Employee-Management-System/backend
python app.py
```

You should see:

```
* Running on http://127.0.0.1:5001
```

Leave this terminal open — the backend must stay running.

> **Note:** Port 5000 is blocked on Mac by AirPlay. That is why we use port 5001.

---

## Step 7 — Start the Frontend

Open another new terminal window and run:

```bash
cd Employee-Management-System/Frontend
python3 -m http.server 8080
```

You should see:

```
Serving HTTP on 0.0.0.0 port 8080
```

Leave this terminal open too.

---

## Step 8 — Open the App in Browser

Open your browser and go to:

```
http://localhost:8080/login.html
```

You will see the login page.

---

## Step 9 — Test the App

### Test 1 — Login

1. Enter username: `admin`
2. Enter password: `admin123`
3. Click **Login**
4. You should be taken to the Employee dashboard

### Test 2 — Add an Employee

1. Fill in the form:
   - Name: `John Doe`
   - Email: `john@example.com`
   - Department: `IT`
   - Salary: `50000`
2. Click **Save**
3. The employee should appear in the table below

### Test 3 — View Employees

The table at the bottom of the page shows all employees from the database. It loads automatically when the page opens.

### Test 4 — Wrong Password

1. Click **Logout**
2. Try logging in with a wrong password
3. You should see **Invalid username or password**

### Test 5 — Direct Access Without Login

1. Without logging in, go to `http://localhost:8080/index.html`
2. You should be automatically redirected to the login page

---

## Step 10 — Test the API Directly (Optional)

You can also test the backend API from the terminal without opening the browser.

**Get all employees:**

```bash
curl http://localhost:5001/employees
```

**Add an employee:**

```bash
curl -X POST http://localhost:5001/add \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane","email":"jane@test.com","department":"HR","salary":45000}'
```

**Test login:**

```bash
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Expected response: `{"success": true}`

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `docker: command not found` | Docker not installed | Install Docker Desktop |
| `pip: command not found` | Python not installed | Install Python 3.12+ |
| `Connection refused` on port 5001 | Flask not running | Run `python app.py` in backend folder |
| `Connection refused` on port 8080 | Frontend server not running | Run `python3 -m http.server 8080` in Frontend folder |
| Login says "Cannot connect to server" | Flask not running | Start the backend first |
| Port 5001 already in use | Another process using it | Run `lsof -i :5001` and kill the process |
| Docker container not starting | Docker Desktop not open | Open Docker Desktop app first |

---

## Folder Overview for Freshers

```
Employee-Management-System/
│
├── backend/            ← Python Flask code (runs on port 5001)
│   ├── app.py          ← Start the server from here
│   ├── config.py       ← Database connection details
│   ├── database.py     ← Opens connection to SQL Server
│   ├── repository.py   ← All SQL queries
│   ├── routes.py       ← API endpoints (URLs)
│   └── requirements.txt← Python packages needed
│
├── Frontend/           ← HTML/CSS/JavaScript (runs on port 8080)
│   ├── login.html      ← Login page
│   ├── login.js        ← Login logic
│   ├── index.html      ← Employee dashboard
│   ├── script.js       ← Employee CRUD logic
│   └── style.css       ← All styles
│
└── EmployeeDB.sql      ← Database schema reference
```

---

## How the 3 Parts Talk to Each Other

```
Browser (port 8080)
    │
    │  HTTP fetch requests
    ▼
Flask API (port 5001)
    │
    │  SQL queries via pymssql
    ▼
SQL Server (port 1433)
```

1. You open the browser → it loads HTML from port 8080
2. JavaScript in the browser sends requests to Flask on port 5001
3. Flask runs SQL queries on SQL Server on port 1433
4. SQL Server returns data → Flask sends it back as JSON → Browser displays it

---

## Stop Everything When Done

```bash
# Stop Flask: press Ctrl+C in the Flask terminal
# Stop Frontend server: press Ctrl+C in the frontend terminal
# Stop SQL Server Docker container:
docker stop sqlserver
```

To start SQL Server again next time (without re-creating it):

```bash
docker start sqlserver
```
