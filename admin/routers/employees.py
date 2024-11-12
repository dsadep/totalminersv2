from flask import Blueprint, render_template, session, url_for, redirect, request
from werkzeug.security import generate_password_hash

from admin.db import database
from admin.db.database import basic_get_all_asc, basic_create
from admin.db.models import Employee
from admin.utils import auth_required

employees_router = Blueprint(name='employees_router', import_name='employees_router')


@employees_router.get('/employees')
@auth_required
def index():
    employees = basic_get_all_asc(Employee)
    return render_template(
        'employees.html',
        employees=employees,
        username=session['username'],
    )


@employees_router.get('/employees/new')
@auth_required
def create_new_employee():
    return render_template('employee_new.html', username=session['username'])


@employees_router.post('/employees/new')
@auth_required
def create_new_employee_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    basic_create(Employee, email=email, username=name, password=generate_password_hash(password))
    return redirect(url_for('employees_router.index'))


@employees_router.post('/employees/<id>/delete')
@auth_required
def delete_employee(id):
    database.delete_employee(id)
    return redirect(url_for('employees_router.index'))
