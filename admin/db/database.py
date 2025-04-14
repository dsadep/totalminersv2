from datetime import datetime, timedelta
from typing import Optional

from admin.db.models.billings import Billing
from admin.db.models.billings_payments import BillingPayment
from admin.db.models.payments import Payment
from admin.db.models.users import User
from admin.db.models.workers import Worker
from admin.service import generate_workers_dict
from admin.utils import hash_to_str
from sqlalchemy import and_, create_engine, Select, delete, func, desc, nulls_last
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, joinedload
from admin.db.models.feedbacks import Feedback
from werkzeug.security import generate_password_hash

from admin.db.base_model import Model
from admin.db.models import Employee, MinerItem, Ticket, Message, Setting
from config import settings

engine = create_engine(settings.get_uri())
Model.metadata.bind = engine
dbsession = sessionmaker(bind=engine, expire_on_commit=False)
session = dbsession()


#
# def get_employee_by_id(id: int) -> Employee | None:
#     candidate = session.execute(Select(Employee).where(Employee.id == id)).scalar_one_or_none()
#     return candidate
#

def create_employee(username, email, password, role) -> Employee | None:
    new_employee = Employee()
    new_employee.email = email
    new_employee.username = username
    new_employee.password = generate_password_hash(password)
    new_employee.role = role
    session.add(new_employee)
    try:
        session.commit()
        session.refresh(new_employee)
        return new_employee
    except IntegrityError as e:
        print(e)
        session.rollback()
        return None


def delete_employee(id: int):
    employee = session.execute(Select(Employee).where(Employee.id == id)).unique().scalar_one_or_none()
    session.delete(employee)
    try:
        session.commit()
    except:
        session.rollback()


def get_all_employees() -> list[Employee]:
    return session.execute(Select(Employee)).scalars().all()


#
# def get_employee_by_username(username: str) -> Employee | None:
#     candidate = session.execute(Select(Employee).where(Employee.username == username)).scalar_one_or_none()
#     return candidate
#

def get_employee_by_email(email: str) -> Employee | None:
    candidate = session.execute(Select(Employee).where(Employee.email == email)).scalar_one_or_none()
    return candidate


#
#
# def get_all_requests() -> list[BuyRequest]:
#     requests = session.execute(Select(BuyRequest)).unique().scalars().all()
#     return requests
#
#
# def get_full_request_by_id(id: int) -> BuyRequest | None:
#     r = session.execute(Select(BuyRequest).where(BuyRequest.id == id)).unique().scalar_one_or_none()
#     return r
#
#
# def update_request_status(id: int, status: str):
#     request = session.execute(Select(BuyRequest).where(BuyRequest.id == id)).unique().scalar_one()
#     request.status = status
#     try:
#         session.commit()
#     except:
#         session.rollback()
#
# def get_all_miners() -> list[MinerItem]:
#     miners = session.execute(Select(MinerItem).order_by(MinerItem.id.asc())).unique().scalars().all()
#     return miners
#
#
# def update_miner(id: int, name, dohod, rashod, profit, hosting_cost, buy_cost, hashrate: str, hidden: bool):
#     miner = session.execute(Select(MinerItem).where(MinerItem.id == id)).unique().scalar_one_or_none()
#     miner.name = name
#     miner.dohod = dohod
#     miner.rashod = rashod
#     miner.profit = profit
#     miner.hosting_cost = hosting_cost
#     miner.buy_cost = buy_cost
#     miner.hashrate = hashrate
#     miner.hidden = hidden
#     try:
#         session.commit()
#     except:
#         session.rollback()


def get_tickets(opened=True) -> list[Ticket]:
    tickets = session.execute(Select(Ticket).where(Ticket.opened == opened)).scalars().all()
    return tickets


def get_ticket_with_messages(id: int) -> Ticket:
    ticket = session.execute(Select(Ticket).where(Ticket.id == id).options(
        joinedload(Ticket.messages)
    ))
    return ticket.unique().scalar_one_or_none()


def add_message_to_ticket(id: int, msg: str, sender: str):
    ticket = session.execute(Select(Ticket).where(Ticket.id == id)).scalar_one_or_none()
    message = Message()
    message.content = msg
    message.sender_name = sender
    message.ticket_id = ticket.id
    message.isCustomerMessage = False
    session.add(message)
    try:
        session.commit()
    except:
        session.rollback()

def get_tickets_sorted_by_date(date: datetime, date_end: datetime):
    query = Select(Ticket).where(
        and_(
            Ticket.created_at >= date,
            Ticket.created_at < date_end
        )
    )
    result = session.execute(query)
    return result.scalars().all()

def get_feedbacks_sorted_by_date(date: datetime, date_end: datetime):
    query = Select(Feedback).where(
        and_(
            Feedback.created >= date,
            Feedback.created < date_end
        )
    )
    result = session.execute(query)
    return result.scalars().all()


def get_top_users_by_hashrate(limit=20):
    subq = (
        session.query(
            Worker.user_id,
            func.sum(MinerItem.hash_rate).label("total_hashrate")
        )
        .join(MinerItem, Worker.miner_item_id == MinerItem.id)
        .filter(Worker.is_active)
        .group_by(Worker.user_id)
        .subquery()
    )

    q = (
        session.query(
            User.id, User.firstname, User.miner_name,
            func.coalesce(subq.c.total_hashrate, 0).label("total_hashrate")
        )
        .outerjoin(subq, User.id == subq.c.user_id)
        .order_by(desc(subq.c.total_hashrate).nullslast(), User.id)
        .limit(limit)
    )

    return [dict(r._mapping) for r in q.all()]

def amount_of_new_users():
    one_month_ago = datetime.now() - timedelta(days=30)

    query = Select(func.count()).select_from(User).where(
        User.created >= one_month_ago
    )

    result = session.execute(query)
    return result.scalar()

def get_non_payments():
    five_days_ago = datetime.now() - timedelta(days=5)

    overdue_billings = (
        session.query(Billing)
        .options(joinedload(Billing.user))
        .filter(
            Billing.type == 'hosting',
            Billing.state != 'completed',
            Billing.created <= five_days_ago
        )
        .all()
    )

    result = []
    for billing in overdue_billings:
        payment_link = (
            session.query(BillingPayment)
            .filter(BillingPayment.billing_id == billing.id)
            .first()
        )

        if not payment_link:
            result.append({
                "billing_id": billing.id,
                "user_id": billing.user.id if billing.user else None,
                "user_name": f"{billing.user.firstname} {billing.user.lastname}" if billing.user else "Unknown",
                "created": billing.created.strftime("%Y-%m-%d %H:%M:%S"),
                "status": billing.state,
                "value": billing.value,
                "currency": billing.currency
            })

    return(result)

def stop_mining_for_user_logic(user_id: int) -> int:
    workers = session.query(Worker).filter(Worker.user_id == user_id).all()
    for worker in workers:
        worker.is_active = False
    session.commit()
    return len(workers)

def resume_mining_for_user_logic(user_id: int) -> int:
    workers = session.query(Worker).filter(Worker.user_id == user_id).all()
    for worker in workers:
        worker.is_active = True
    session.commit()
    return len(workers)

def get_settings_value(key: str) -> str:
    result = session.query(Setting).filter(Setting.key == key).first()
    return result.value if result else "0"

def get_main_page_stats(days: int | None):
    date_ago = datetime.now() - timedelta(days=days)
    online_workers = session.query(Worker).filter(Worker.is_active == True).all()
    offline_workers = session.query(Worker).filter(Worker.is_active == False).all()
    total_hashrate = (
        session.query(func.sum(MinerItem.hash_rate))
        .outerjoin(Worker, Worker.miner_item_id == MinerItem.id)
        .scalar()
    )
    electricity_cost = float(get_settings_value('electricity_cost'))
    hashrate_kw = float(get_settings_value('hash_rate_electricity_consumption'))

    kw = float(total_hashrate) * hashrate_kw / 1e12
    electricity_price = round(kw * electricity_cost, 2)
    if days != 0:
        hosting_income = (
            session.query(func.sum(Billing.value_usd))
            .filter(
                Billing.type == 'hosting',
                Billing.state == 'completed',
                Billing.created >= date_ago
            )
            .scalar()
        ) or 0
        hosting_profit = round(hosting_income - electricity_price)

        sales = (
            session.query(func.sum(Billing.value_usd))
            .filter(
                Billing.type == 'buy_request',
                Billing.state == 'completed',
                Billing.created >= date_ago
            )
            .scalar()
        ) or 0
    else:
        hosting_income = (
            session.query(func.sum(Billing.value_usd))
            .filter(
                Billing.type == 'hosting',
                Billing.state == 'completed',
            )
            .scalar()
        ) or 0
        hosting_profit = round(hosting_income - electricity_price)

        sales = (
            session.query(func.sum(Billing.value_usd))
            .filter(
                Billing.type == 'buy_request',
                Billing.state == 'completed',
            )
            .scalar()
        ) or 0


    if days == 0:
        feedback_requests = session.query(Feedback).all()
        new_tickets = session.query(Ticket).all()
        client_income = session.query(func.sum(Payment.value)).filter(
            Payment.type == 'reward',
        ).scalar() or 0
        client_expence = session.query(func.sum(Payment.value)).filter(
            Payment.type == 'hosting'
        ).scalar() or 0
    else:
        feedback_requests = session.query(Feedback).filter(Feedback.created >= date_ago).all()
        new_tickets = session.query(Ticket).filter(Ticket.created_at >= date_ago).all()
        client_income = session.query(func.sum(Payment.value)).filter(
            Payment.type == 'reward',
            Payment.created >= date_ago
        ).scalar() or 0
        client_expence = session.query(func.sum(Payment.value)).filter(
            Payment.type == 'hosting',
            Payment.created >= date_ago
        ).scalar() or 0

    return {
        'online_workers': len(online_workers),
        'offline_workers': len(offline_workers),
        'total_hashrate': hash_to_str(total_hashrate) if total_hashrate != 0 else hash_to_str(0),
        'kw': round(kw, 2),
        'electricity_cost': electricity_price,
        'feedbacks': len(feedback_requests),
        'tickets': len(new_tickets),
        'hosting_profit': hosting_profit,
        'sales_total': round(float(sales), 2),
        'client_income': round(float(client_income), 2),
        'client_expence': round(abs(float(client_expence)), 2),
        'client_profit': round(float(client_income)-abs(float(client_expence)), 2)
    }
    
    #offline_workers 
    #hash


#
# def create_worker(
#         item_name,
#         worker_id,
#         worker_name,
#         hashrate,
#         item_id,
#         user_id,
# ) -> Worker:
#     worker = Worker()
#     worker.item_name = item_name
#     worker.worker_id = worker_id
#     worker.worker_name = worker_name
#     worker.user_id = user_id
#     worker.hashrate = hashrate
#     worker.item_id = item_id
#     session.add(worker)
#     session.commit()
#     session.refresh(worker)
#     return worker
#




def create_db():
    Model.metadata.create_all(bind=engine)


"""
BASIC
"""


def basic_create(db_model, **obj_data):
    db_obj = db_model(**obj_data)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def basic_get(db_model, **filters):
    result = session.execute(Select(db_model).filter_by(**filters))
    return result.scalars().first()


def basic_get_all(db_model, **filters):
    result = session.execute(Select(db_model).filter_by(**filters).order_by(db_model))
    return result.scalars().all()


def basic_get_all_asc(db_model, **filters):
    result = session.execute(Select(db_model).filter_by(**filters).order_by(db_model.id.asc()))
    return result.scalars().all()


def basic_get_all_desc(db_model, **filters):
    result = session.execute(Select(db_model).filter_by(**filters).order_by(db_model.id.desc()))
    return result.scalars().all()


def basic_update(db_obj: Model, **obj_in_data):
    for field, value in obj_in_data.items():
        setattr(db_obj, field, obj_in_data[field])
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def basic_delete(db_model, id_: int):
    session.execute(delete(db_model).where(db_model.id == id_))
    session.commit()


"""    
SETTINGS
"""


def setting_get(key: str, default=None) -> Optional[str]:
    setting = basic_get(db_model=Setting, key=key)
    if not setting:
        return default
    return setting.value


def setting_update(key: str, value) -> Optional[str]:
    setting = basic_get(db_model=Setting, key=key)
    if setting:
        setting = basic_update(db_obj=setting, value=value)
    else:
        setting = basic_create(db_model=Setting, key=key, value=value)
    return setting
