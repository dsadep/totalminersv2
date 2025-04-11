from flask import Blueprint, request, jsonify

from admin.db.database import setting_get, setting_update
from admin.utils import admin_only, auth_required

settings_router = Blueprint(name='settings_router', import_name='settings_router')


@settings_router.get('/settings')
@auth_required
@admin_only
def get_settings():
    """Получение всех настроек"""
    data = {
        # Payment
        'payment_bank_card': setting_get(key='payment_bank_card'),
        'payment_btc': setting_get(key='payment_btc'),
        'payment_usdt': setting_get(key='payment_usdt'),
        # Calculation
        'invest_min': float(setting_get(key='invest_min')),
        'invest_max': float(setting_get(key='invest_max')),
        'electricity_cost': float(setting_get(key='electricity_cost')),
        'hash_rate_electricity_consumption': float(setting_get(key='hash_rate_electricity_consumption')),
        'hash_rate_cost': float(setting_get(key='hash_rate_cost')),
        # Other
        'miner_banner': setting_get(key='miner_banner'),
        'home_page_youtube_link': setting_get(key='home_page_youtube_link'),
        'payback_min': setting_get(key='payback_min'),
        'payback_max': setting_get(key='payback_max'),
    }
    return jsonify(data)


@settings_router.post('/settings/update')
@auth_required
@admin_only
def update_settings():
    """Обновление настроек"""
    try:
        # Payment
        setting_update(key='payment_bank_card', value=request.form['payment_bank_card'])
        setting_update(key='payment_btc', value=request.form['payment_btc'])
        setting_update(key='payment_usdt', value=request.form['payment_usdt'])
        # Calculation
        setting_update(key='invest_min', value=request.form['invest_min'])
        setting_update(key='invest_max', value=request.form['invest_max'])
        setting_update(key='electricity_cost', value=request.form['electricity_cost'])
        setting_update(key='hash_rate_electricity_consumption', value=request.form['hash_rate_electricity_consumption'])
        setting_update(key='hash_rate_cost', value=request.form['hash_rate_cost'])
        # Other
        setting_update(key='miner_banner', value=request.form['miner_banner'])
        setting_update(key='home_page_youtube_link', value=request.form['home_page_youtube_link'])
        setting_update(key='payback_min', value=request.form['payback_min'])
        setting_update(key='payback_max', value=request.form['payback_max'])
        
        return jsonify({"message": "Настройки успешно обновлены"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
