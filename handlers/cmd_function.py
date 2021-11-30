from aiogram import types
from aiogram.utils.exceptions import Throttled

from config import reg_text, auth_text
from database import db_user_info, db_user_reg, db_insert_admin, db_delete_admin, db_select_admins, top_up_select
from loader import dp, bot
from keyboards import main_start

@dp.message_handler(commands=['start'])
@dp.throttled(lambda msg, loop, *args, **kwargs: loop.create_task(bot.send_message(msg.from_user.id, "Перестаньте "
                                                                                                     "флудить!")),
              rate=5)
async def start_for_user(msg):
    if not db_user_info(msg.chat.id):
        db_user_reg(msg)
        await msg.answer(reg_text, reply_markup=await main_start(msg.chat.id))
    else:
        await msg.answer(auth_text, reply_markup=await main_start(msg.chat.id))


@dp.message_handler(commands=['info'])
async def info_user(msg):
    data = msg.text.split()
    if len(data) > 1:
        text = ''
        top_up_user = top_up_select(msg.chat.id)
        for info in top_up_user:
            text += f'{info[0]}, {info[1]}, {info[2]}\n'
        await msg.answer(text)
    else:
        await msg.answer('*SYSTEM:* /info [[user_id]]')


@dp.message_handler(commands=['add_admin'])
async def add_admin(msg):
    if db_select_admins(msg.chat.id):
        data = msg.text.split()
        if len(data) > 1:
            new_admin_id = data[1]
            if db_user_info(new_admin_id):
                db_insert_admin(new_admin_id)
                await msg.answer('*SYSTEM:* Администратор успешно добавлен')
            else:
                await msg.answer('*SYSTEM:* Пользователь не найден.\n\n'
                                 '*Будущий администратор должен быть зарегистрирован с помощью команды /start*')
        else:
            await msg.answer('*SYSTEM:* /add\\_admin [[user_id]]')


@dp.message_handler(commands=['del_admin'])
async def del_admin(msg):
    if db_select_admins(msg.chat.id):
        data = msg.text.split()
        if len(data) > 1:
            old_admin_id = data[1]
            if db_user_info(old_admin_id):
                db_delete_admin(old_admin_id)
                await msg.answer('*SYSTEM:* Администратор успешно удален')
            else:
                await msg.answer('*SYSTEM:* Пользователь не найден.')
        else:
            await msg.answer('*SYSTEM:* /del\\_admin [[user_id]]')
