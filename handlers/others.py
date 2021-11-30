from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageCantBeDeleted
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers import start_for_user
from loader import dp, bot


# Обработка всех колбэков которые потеряли стейты после перезапуска скрипта
@dp.callback_query_handler(text="...", state="*")
async def processing_missed_callback(call: CallbackQuery):
    await call.answer(cache_time=60)


@dp.callback_query_handler(text='CANCEL', state='*')
@dp.message_handler(commands="cancel", state="*")
@dp.message_handler(Text(equals="отмена" or 'Отмена', ignore_case=True), state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено")


# Обработка всех колбэков которые потеряли стейты после перезапуска скрипта
@dp.callback_query_handler(state="*")
async def processing_missed_callback(call: CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except MessageCantBeDeleted:
        pass
    await bot.send_message(call.from_user.id, "❌ *Данные не были найдены из-за перезапуска скрипта.\n"
                                              "♻ Выполните действие заново.*")


# Обработка всех неизвестных сообщений
@dp.message_handler()
async def processing_missed_messages(message: types.Message):
    await message.answer("♦ *Неизвестная команда.*\n"
                         "▶ Введите /start")
