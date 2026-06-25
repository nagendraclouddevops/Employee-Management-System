from database import get_connection
from werkzeug.security import check_password_hash


def get_user_by_username(username):
    with get_connection() as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute("SELECT Id, Username, PasswordHash FROM Users WHERE Username=%s", (username,))
            return cursor.fetchone()


def verify_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user["PasswordHash"], password):
        return True
    return False


def get_all_employees():
    with get_connection() as conn:
        with conn.cursor(as_dict=True) as cursor:
            cursor.execute("SELECT Id, Name, Email, Department, Salary FROM Employees")
            return cursor.fetchall()


def add_employee(name, email, department, salary):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Employees (Name, Email, Department, Salary) VALUES (%s, %s, %s, %s)",
                (name, email, department, salary),
            )
        conn.commit()


def update_employee(emp_id, name, email, department, salary):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Employees SET Name=%s, Email=%s, Department=%s, Salary=%s WHERE Id=%s",
                (name, email, department, salary, emp_id),
            )
        conn.commit()


def delete_employee(emp_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM Employees WHERE Id=%s", (emp_id,))
        conn.commit()
