from typing import Optional

from sqlalchemy import create_engine, Select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, joinedload
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

def create_employee(username, email, password) -> Employee | None:
    new_employee = Employee()
    new_employee.email = email
    new_employee.username = username
    new_employee.password = generate_password_hash(password)
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


#
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
