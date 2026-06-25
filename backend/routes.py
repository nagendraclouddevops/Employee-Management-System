from flask import Blueprint, request, jsonify
import repository

bp = Blueprint("employees", __name__)


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if repository.verify_user(data.get("username"), data.get("password")):
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid username or password"}), 401


@bp.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(repository.get_all_employees())


@bp.route("/add", methods=["POST"])
def add_employee():
    data = request.get_json()
    repository.add_employee(
        data["name"], data["email"], data["department"], data["salary"]
    )
    return jsonify({"message": "Employee added"}), 201


@bp.route("/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    data = request.get_json()
    repository.update_employee(
        emp_id, data["name"], data["email"], data["department"], data["salary"]
    )
    return jsonify({"message": "Employee updated"})


@bp.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    repository.delete_employee(emp_id)
    return jsonify({"message": "Employee deleted"})
