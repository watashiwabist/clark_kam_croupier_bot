import asyncio
import datetime
import random
import string
import time

import requests
from SimpleQIWI import QApi
from pyqiwip2p import QiwiP2P

from database import db_select_admins, db_select_id_admins, db_get_merchant_token, db_check_comments
from loader import bot


async def time_pay(msg):
    try:
        COUNT_SEC = 3000
        time_now = time.mktime(datetime.datetime.now().timetuple())
        while True:
            await asyncio.sleep(COUNT_SEC / 10)
            temp_time = time.mktime(datetime.datetime.now().timetuple())  # время в цикле (в секундах)
            if temp_time > (time_now + COUNT_SEC):  # true если время в цикле больше чем Present Time + count Sec
                await bot.delete_message(msg.chat.id, msg.message_id + 1)
                break
    except Exception as e:
        pass
    else:
        await bot.send_message(msg.chat.id, 'Срок действия счета на оплату истек.')


# async def connect_yoomoney(token):
#     try:
#         client = Client(token)
#         user = client.account_info()
#         return user
#     except:
#         return False


async def connect_qiwi2(token):
    try:
        client = QApi(token=token, phone='')
        client.balance
        return True
    except:
        return False


async def pay_qiwi(amount, account):
    token = db_get_merchant_token('qiwi2')
    try:
        client = QApi(token=token, phone='')
        if client.balance < amount:
            raise Exception('not_enough_money')
        client.pay(account=account, amount=amount)
        return True
    except Exception as e:
        return False


async def yoo_balance():
    token = db_get_merchant_token('yoomoney')
    response = requests.post(
        'https://yoomoney.ru/api/account-info',
        headers={'Authorization': f'Bearer {token}',
                 'Host': 'yoomoney.ru',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    )
    content = response.json()
    return content['balance']


async def pay_yoo(amount, account):
    try:
        token = db_get_merchant_token('yoomoney')
        balance = await yoo_balance()
        if balance < amount:
            raise Exception('not_enough_money')
        response = requests.post(
            'https://yoomoney.ru/api/request-payment',
            headers={'Authorization': f'Bearer {token}',
                     'Host': 'yoomoney.ru',
                     'Content-Type': 'application/x-www-form-urlencoded'},
            params=f'pattern_id=p2p&to={account}&amount={amount}'
        )
        content = response.json()
        return content
    except:
        return False


# async def create_yoo_bill(sum):
#     token = db_get_merchant_token('yoomoney')
#     try:
#         client = Client(token)
#         user = client.account_info()
#         comment = await get_payment_comment()
#         quickpay = Quickpay(
#             receiver=f"{user.account}",
#             quickpay_form="shop",
#             targets="Пополнение баланса",
#             paymentType="SB",
#             sum=sum,
#             label=comment,
#             comment=comment
#         )
#         return quickpay
#     except Exception as e:
#         print(f'misc.misc.create_yoo_bill: {e}')


async def get_payment_comment():
    passwd = list("1234567890")
    random.shuffle(passwd)
    comment = "".join([random.choice(passwd) for x in range(30)])
    while not db_check_comments(comment):
        comment = "".join([random.choice(passwd) for x in range(30)])
    return comment


async def create_qiwi_bill(sum):
    token = db_get_merchant_token('qiwi')
    try:
        p2p = QiwiP2P(auth_key=token)
        qiwi_comment = await get_payment_comment()
        new_bill = p2p.bill(comment=qiwi_comment, amount=int(sum), lifetime=15)
        return new_bill
    except Exception as e:
        print(f'misc.create_qiwi_bill: {e}')


async def qiwi_bill_info(bill_id):
    token = db_get_merchant_token('qiwi')
    try:
        p2p = QiwiP2P(auth_key=token)
        info = p2p.check(bill_id)
        return info
    except Exception as e:
        print(f'misc.qiwi_bill_info: {e}')


def username(name):
    return name.replace("_", "\_")


async def admin_msg(level, text=None):
    try:
        if level == 2:
            admins = db_select_id_admins()
        else:
            admins = db_select_admins()
        for b in range(len(admins)):
            try:
                await bot.send_message(admins[b][0], text)
            except Exception as e:
                print(f'handlers.user_function.user_check_pay.admin_message: {e}\n'
                      f'Возможно ошибка из-за того что администратор не прописал /start')
    except Exception as e:
        print(f'misc.admin_msg: {e}')


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for _ in range(length))
    return rand_string


async def sleep(sec):
    time.sleep(sec)


def count_players(lobby_info):
    cnt = 0
    for player in range(3, 8):
        if lobby_info[player] is not None:
            cnt += 1
        else:
            break
    return cnt
