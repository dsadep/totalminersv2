from admin.db.database import get_main_page_stats
from admin.utils import auth_required
from flask import Blueprint, jsonify

main_page_router = Blueprint(name = 'main_page_router', import_name = 'main_page_router')

@main_page_router.get('/main')
@auth_required
def main_page():
    stats = get_main_page_stats(0)
    return stats

@main_page_router.get('/main/daily')
@auth_required
def main_page_daily():
    stats = get_main_page_stats(1)
    return stats

@main_page_router.get('/main/weekly')
@auth_required
def main_page_weekly():
    stats = get_main_page_stats(7)
    return stats

@main_page_router.get('/main/monthly')
@auth_required
def main_page_monthly():
    stats = get_main_page_stats(30)
    return stats

