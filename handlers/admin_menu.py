from aiogram.types import CallbackQuery
from database import db_select_admins, db_get_fee, db_get_bot_status
from keyboards import coupon_settings, cancel, choice_admin, change_api, statbot
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


from states import spam, fee


class isAdmins(BoundFilter):
    async def check(self, message: types.Message):
        if db_select_admins(message.from_user.id) is None:
            return False
        else:
            return True

@dp.message_handler(isAdmins(), text='Сделать рассылку')
async def get_spam(msg: types.Message):
    await msg.answer('Ожидаю от вас пост для рассылки', reply_markup=await cancel())
    await spam.post.set()

@dp.message_handler(isAdmins(), text='Комиссия')
async def set_fee(msg: types.Message):
    current_fee = db_get_fee()
    await msg.answer(f'Текущая комиссия {current_fee}%.\n Отправьте желаемую комиссию', reply_markup=await cancel())
    await fee.fee.set()
#     state


@dp.message_handler(isAdmins(), text='Купоны')
async def settings_coupon(msg: types.Message):
    await msg.answer('Настройка купонов', reply_markup=await coupon_settings())

@dp.message_handler(isAdmins(), text='Состояние')
async def bot_status(msg: types.Message):
    cur_status = db_get_bot_status()
    state = 'включен' if cur_status == 1 else 'выключен'
    await msg.answer(f'Бот в данный момент {state}, изменить состояние?', reply_markup=await statbot())


@dp.message_handler(isAdmins(), text='Сменить API')
async def change_wallets(msg: types.Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer('Где заменить API?', reply_markup=await change_api())