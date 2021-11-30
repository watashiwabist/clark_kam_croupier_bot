import asyncio
import datetime
import random
import string
import time

from coinbase.wallet.client import Client

from database import db_select_client, db_select_admins, db_select_id_admins
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


async def coinbase_client():
    coinbase = db_select_client()
    client = Client(coinbase[0], coinbase[1])
    return client

async def get_USD_LTC(amount):
    client = await coinbase_client()
    curs = client.get_spot_price(currency_pair='LTC-USD')['amount']
    price = round((float(amount) / float(curs)), 8)
    return price


async def get_LTC_USD(amount):
    client = await coinbase_client()
    curs = client.get_spot_price(currency_pair='LTC-USD')['amount']
    amount = round(float(amount) * float(curs), 2)
    return amount


async def cur_transfer(amount):
    try:
        client = await coinbase_client()
        price = await get_USD_LTC(amount)
        user_id = client.get_accounts()[0]['id']
        address_info = client.create_address(user_id)
        data = [price, address_info['address'], address_info['id']]
        return data
    except Exception as e:
        print(f'misc.cur_transfer: {e}')


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
