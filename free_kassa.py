import hashlib
import hmac
import json
import time

import requests

from config import shop_id, freekassa_api


def create_order(price: int, secret_word, merchant_id, order_id):
    sign = hashlib.md5(f'{shop_id}:{price}:{secret_word}:RUB:{order_id}'.encode('utf-8')).hexdigest()
    return {
        'id': str(order_id),
        'sign': sign,
        'url': f'https://pay.freekassa.ru/?m={merchant_id}&oa={price}&o={order_id}&s={sign}&currency=RUB'
    }


def get_sign(json_data):
    sorted_json = dict(sorted(json_data.items(), key=lambda x: x[0]))  # сортировка значений
    msg = "|".join(map(str, sorted_json.values()))  # конкатенация значений
    sign = hmac.new(freekassa_api.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).hexdigest()  # генерация подписи
    sorted_json.update(signature=sign)
    return sorted_json


def get_balance():
    json_data = {
        'shopId': shop_id,
        'nonce': time.time_ns(),
    }
    json_data = get_sign(json_data)  # добавление подписи
    r = requests.post('https://api.freekassa.ru/v1/balance', json=json_data)
    json_resp = json.loads(r.text)
    return json_resp


def bill_info(bill_id=None):
    if bill_id is not None:
        json_data = {
            'shopId': shop_id,
            'nonce': time.time_ns(),
            'paymentId': bill_id,
        }
    else:
        json_data = {
            'shopId': shop_id,
            'nonce': time.time_ns()
        }
    json_data = get_sign(json_data)  # добавление подписи
    r = requests.post('https://api.freekassa.ru/v1/orders', json=json_data)
    json_resp = json.loads(r.text)
    return json_resp


def withdraw_order(amount, account, payment_id, currency='RUB'):
    json_data = {
        'shopId': shop_id,
        'nonce': time.time_ns(),
        'i': payment_id,
        'account': account,
        'amount': amount,
        'currency': currency,
    }
    json_data = get_sign(json_data)
    r = requests.post('https://api.freekassa.ru/v1/withdrawals/create', json=json_data)
    json_resp = json.loads(r.text)
    return json_resp


def available_payments():
    json_data = {
        'shopId': shop_id,
        'nonce': time.time_ns(),
    }
    json_data = get_sign(json_data)  # добавление подписи
    r = requests.post('https://api.freekassa.ru/v1/withdrawals/currencies', json=json_data)
    json_resp = json.loads(r.text)
    return json_resp


def get_currency(method):
    currenct = {
        'CARD': 36,
    }
    currency = 63 if method == 'QIWI' else 0
    currency = 94 if method == 'CARD' else currency
    currency = 114 if method == 'PAYEER' else currency
    currency = 64 if method == 'PERFECT' else currency
    return currency
