from flask import Flask, session, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash

from admin.db import database
from admin.db.database import basic_get
from admin.db.models import Employee
from admin.routers.billings import billings_router
from admin.routers.buy_requests import buy_requests_router
from admin.routers.employees import employees_router
from admin.routers.feedbacks import feedbacks_router
from admin.routers.miners import miners_router
from admin.routers.miners_items_categories import miners_items_categories_router
from admin.routers.settings import settings_router
from admin.routers.tickets import tickets_router
from admin.routers.users import users_router
from admin.routers.worker import workers_router
from admin.routers.discounts import discounts_router
from admin.utils import auth_required
from config import settings
from logger import config_logger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

app.register_blueprint(users_router)
app.register_blueprint(employees_router)
app.register_blueprint(buy_requests_router)
app.register_blueprint(billings_router)
app.register_blueprint(miners_router)
app.register_blueprint(tickets_router)
app.register_blueprint(settings_router)
app.register_blueprint(workers_router)
app.register_blueprint(miners_items_categories_router)
app.register_blueprint(feedbacks_router)
app.register_blueprint(discounts_router)


@app.get('/')
@app.get('/index')
@auth_required
def index():
    return redirect(url_for('users_router.index'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form.get('email')
    password = request.form.get('password')
    employee = basic_get(Employee, email=email)
    if employee is None:
        return render_template('login.html')
    if check_password_hash(employee.password, password):
        session['logged'] = True
        session['username'] = employee.username
        session['role'] = employee.role.value
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
@auth_required
def logout():
    session.clear()
    return redirect(url_for('login_page'))


@app.get('/test')
def create_test_admin():
    database.create_employee(
        'admin',
        'example@example.com',
        'qwerty21'
    )
    return 'ok'


@app.get('/initdb')
def initdb():
    database.create_db()
    return 'ok'


def create_app():
    config_logger()
    return app
