from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



async def cancel():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Отмена', callback_data='CANCEL'))
    return markup
