from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from admin.db import database
from admin.db.database import basic_get_all_asc, basic_create, basic_get
from admin.db.models import Employee
from admin.utils import auth_required

employees_router = Blueprint(name='employees_router', import_name='employees_router')


@employees_router.get('/employees')
@auth_required
def get_all_employees():
    """Получение всех сотрудников."""
    employees = basic_get_all_asc(Employee)
    return jsonify({
        'employees': [employee.as_dict() for employee in employees],
    }), 200


@employees_router.post('/employees/new')
@auth_required
def create_new_employee():
    """Создание нового сотрудника."""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not name or not email or not password:
        return jsonify({"error": "Нелостаточно данных"}), 400
    hashed_password = generate_password_hash(password)
    employee = basic_create(Employee, email=email, username=name, password=hashed_password)

    return jsonify({"message": "Сотрудник успешно создан", "employee_id": employee.id}), 201



@employees_router.post('/employees/<int:id>/delete')
@auth_required
def delete_employee(id):
    """Удаление сотрудника по ID."""
    employee = basic_get(Employee, id=id)
    if not employee:
        return jsonify({"error": "Сотрудник не найден"}), 404
    database.delete_employee(id)
    return jsonify({"message": "Сотрудник успешно удален"}), 200

