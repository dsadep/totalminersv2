from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import check_password_hash
import datetime

from admin.db import database
from admin.db.database import basic_get, basic_create
from admin.db.models import Employee, User
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
from admin.utils import auth_required, generate_token
from config import settings
from logger import config_logger

app = Flask(__name__)
CORS(app, supports_credentials=True)
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
def index():
    return jsonify({"message": "OK!"})


@app.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    print('Полученные данные', data)
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    employee = basic_get(Employee, email=email)
    
    if employee is None:
        print("User not found")
        return jsonify({"error": "Invalid credentials"}), 401

    password = password.strip("'\"")

    if not check_password_hash(employee.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(employee.email)
    return jsonify({"token": token})




@app.route('/logout', methods=['POST'])
@auth_required
def api_logout():
    return jsonify({"message": "Logged out successfully"})


@app.get('/test')
def create_test_admin():
    database.create_employee(
        'admin',
        'example@example.com',
        'qwerty21'
    )
    return jsonify({"message": "Test admin created"})


@app.get('/initdb')
def initdb():
    database.create_db()
    return jsonify({"message": "Database initialized"})

@app.post('/create_test_user')
@auth_required
def create_test_user():
    """Создание тестового пользователя"""
    
    # Получение данных из запроса
    data = request.get_json()
    
    # Проверка, что все обязательные поля есть в запросе
    required_fields = [
        'firstname', 'lastname', 'phone', 'email', 'password',
        'telegram', 'country', 'address', 'inn', 'profile_type',
        'wallet', 'miner_name', 'miner_id', 'wallet_id', 'lang'
    ]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Отсутствует обязательное поле: {field}"}), 400
    
    user = basic_create(
        User,
        firstname=data['firstname'],
        lastname=data['lastname'],
        phone=data['phone'],
        email=data['email'],
        password=data['password'],
        telegram=data['telegram'],
        country=data['country'],
        address=data['address'],
        inn=data['inn'],
        profile_type=data['profile_type'],
        wallet=data['wallet'],
        miner_name=data['miner_name'],
        miner_id=data['miner_id'],
        wallet_id=data['wallet_id'],
        lang=data['lang'],
        created=datetime.datetime.now()
    )
    
    return jsonify({
        "message": "Тестовый пользователь создан",
        "user": {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "phone": user.phone,
            "email": user.email,
            "telegram": user.telegram,
            "country": user.country,
            "address": user.address,
            "inn": user.inn,
            "profile_type": user.profile_type,
            "wallet": user.wallet,
            "miner_name": user.miner_name,
            "miner_id": user.miner_id,
            "wallet_id": user.wallet_id,
            "lang": user.lang,
            "created": user.created.strftime('%Y-%m-%d %H:%M:%S')
        }
    }), 201

def create_app():
    config_logger()
    return app
