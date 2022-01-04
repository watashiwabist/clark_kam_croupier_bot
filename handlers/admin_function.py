# -*- coding: UTF-8 -*-
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from database import db_insert_coupon, \
    db_delete_coupon, db_select_all_user, db_set_fee, db_set_merchant_token, db_get_bot_status, db_set_bot_status
from keyboards import coupon_info, cancel
from loader import dp, bot
from misc import generate_random_string, connect_qiwi2
from states import settAdmin, spam, fee, qiwi, yoomoney, freekassa, qiwi2


####################################################################################################
# CALLBACK HANDLER
####################################################################################################
# -------------------COUPON-----------------------

@dp.callback_query_handler(text='ADD_COUPON', state='*')
async def set_add_coupon(call: CallbackQuery):
    await call.message.answer('Введите *сумму* купона:')
    await settAdmin.addCoupon.set()


@dp.callback_query_handler(text='INFO_COUPON', state='*')
async def set_info_coupon(call: CallbackQuery):
    await call.message.answer('Для удаления купона - нажмите на него', reply_markup=await coupon_info())


@dp.callback_query_handler(text_startswith='COUPON:', state='*')
async def set_del_coupon(call: CallbackQuery):
    coupon_id = call.data[7:]
    db_delete_coupon(coupon_id)
    await call.answer('Купон успешно удален')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                        reply_markup=await coupon_info())


####################################################################################################
# MESSAGE HANDLER
####################################################################################################


@dp.message_handler(state=settAdmin.addCoupon)
async def add_coupon(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer('Введите *сумму* купона:')
    else:
        if ';' in msg.text:
            await msg.answer('Введите *сумму* купона:')
        else:
            gen_coup = generate_random_string(6)
            db_insert_coupon(gen_coup, msg.text)
            await msg.answer(f'Купон - *{gen_coup}* успешно создан')
            await state.finish()


@dp.message_handler(content_types=['photo', 'text'], state=spam.post)
async def post_for_user(msg: types.Message, state: FSMContext):
    users = db_select_all_user()
    count = 0
    if msg.photo:
        for a in range(len(users)):
            # noinspection PyBroadException
            try:
                count += 1
                await bot.send_photo(users[a][0], msg.photo[0].file_id, caption=msg.caption)
            except:
                pass
    else:
        for a in range(len(users)):
            print(users[a][0])
            # noinspection PyBroadException
            try:
                count += 1
                await bot.send_message(users[a][0], msg.text)
            except:
                pass
    await msg.answer(f'*Рассылка прошла успешно*\n'
                     f'*Отправленных сообщений:* {count}')
    await state.finish()


@dp.callback_query_handler(text_startswith='CHANGE_WITHDRAW_QIWI')
async def change_qiwi(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отправьте новый token QIWI кошелька')
    await qiwi2.set_qiwi.set()


@dp.callback_query_handler(text_startswith='CHANGE_QIWI')
async def change_qiwi(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отправьте новый token QIWI кошелька')
    await qiwi.set_qiwi.set()


@dp.callback_query_handler(text_startswith='CHANGE_YOOMONEY')
async def change_qiwi(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отправьте новый token YOOMONEY кошелька')
    await yoomoney.set_api.set()


@dp.callback_query_handler(text_startswith='CHANGE_FREEKASSA')
async def change_qiwi(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отправьте новый token FREEKASSA кошелька')
    await freekassa.set_api.set()


@dp.callback_query_handler(text_startswith='CHANGE_BOT_STATUS')
async def change_bot_status(call: CallbackQuery):
    cur_status = db_get_bot_status()
    db_set_bot_status((cur_status + 1) % 2)
    await call.message.answer('Состояние бота успешно изменено!')


@dp.message_handler(state=fee.fee)
async def fee_for_win(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer('Отправьте число')
        return
    db_set_fee(int(msg.text))
    await msg.answer('Комиссия успешно установлена.')
    await state.finish()


@dp.message_handler(state=qiwi.set_qiwi)
async def qiwi_state(msg: types.Message, state: FSMContext):
    db_set_merchant_token(msg.text, 'qiwi')
    await msg.answer('QIWI кошелек успешно установлен\n')
    await state.finish()


@dp.message_handler(state=qiwi2.set_qiwi)
async def qiwi_state(msg: types.Message, state: FSMContext):
    if await connect_qiwi2(msg.text):
        db_set_merchant_token(msg.text, 'qiwi2')
        await msg.answer('QIWI кошелек успешно установлен\n')
        await state.finish()
    else:
        await msg.answer('Кажется вы ввели неверный токен.\nПопробуйте еще раз.', reply_markup=await cancel())


