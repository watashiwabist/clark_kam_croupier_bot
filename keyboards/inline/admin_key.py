from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import value
from database import db_select_coupon, db_select_admins, db_user_info


async def coupon_settings():
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('Создать купон', callback_data='ADD_COUPON')
    button_2 = InlineKeyboardButton('Активные купоны', callback_data='INFO_COUPON')
    markup.add(button_1, button_2)
    return markup


async def coupon_info():
    coupon = db_select_coupon()
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        *[InlineKeyboardButton(f'{coupon[a][1]} - {coupon[a][2]} {value}', callback_data=f'COUPON:{coupon[a][0]}') for a
          in range(len(coupon))])
    return markup


async def statbot():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton('Да', callback_data='CHANGE_BOT_STATUS')
    )
    return markup


async def choice_admin():
    markup = InlineKeyboardMarkup(3)
    admins = db_select_admins()
    markup.add(
        *[InlineKeyboardButton(f'{db_user_info(_[0])[1]} | {_[0]}', callback_data=f'STATISTIC:{_[0]}') for _ in admins])
    return markup


async def change_api():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton('QIWI получение', callback_data='CHANGE_QIWI'),
        InlineKeyboardButton('QIWI вывод', callback_data='CHANGE_WITHDRAW_QIWI'),
    )
    return markup