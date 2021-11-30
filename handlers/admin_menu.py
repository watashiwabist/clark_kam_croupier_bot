from aiogram.types import CallbackQuery
from database import db_select_admins
from keyboards import product_settings, coupon_settings, catalog_settings, cancel, choice_admin
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from misc import coinbase_client
from states import changeCoinbase, transaction, spam


class isAdmins(BoundFilter):
    async def check(self, message: types.Message):
        if db_select_admins(message.from_user.id) is None:
            return False
        else:
            return True


@dp.message_handler(isAdmins(), text='Настройка продуктов')
async def settings_product(msg: types.Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer('Настройка продуктов', reply_markup=await product_settings())


@dp.message_handler(isAdmins(), text='Настройка каталога')
async def settings_catalog(msg: types.Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer('Настройка каталога', reply_markup=await catalog_settings())


@dp.message_handler(isAdmins(), text='Сделать рассылку')
async def get_spam(msg: types.Message):
    await msg.answer('Ожидаю от вас пост для рассылки')
    await spam.post.set()


#     state


@dp.message_handler(isAdmins(), text='Купоны')
async def settings_coupon(msg: types.Message):
    await msg.answer('Настройка купонов', reply_markup=await coupon_settings())


@dp.message_handler(isAdmins(), text='Сменить API')
async def change_api(msg: types.Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer('Введите ключ API в формате token;token')
    await changeCoinbase.token.set()


@dp.message_handler(isAdmins(), text='Перевести')
async def admin_transaction(msg: types.Message):
    client = await coinbase_client()
    user_id = client.get_accounts()[0]['id']
    balance = client.get_account(user_id)['native_balance']
    await msg.answer(f'Баланс: {str(balance)[4:]} $\n\n'
                     f'*Введите LTC счет для перевода средств*', reply_markup=await cancel())
    await transaction.ltc_address.set()


@dp.message_handler(isAdmins(), text='Статистика')
async def admin_statistics(msg: types.Message):
    await msg.answer('Выберите администратора для просмотра статистики', reply_markup=await choice_admin())


# state


@dp.callback_query_handler(text='BACK_SETTINGS_CATALOG')
async def set_del_subcatalog(call: CallbackQuery):
    await bot.edit_message_text('Настройка каталога', call.from_user.id, call.message.message_id,
                                reply_markup=await catalog_settings())


@dp.callback_query_handler(text='BACK_SETTINGS_PRODUCT')
async def set_del_subcatalog(call: CallbackQuery):
    await bot.edit_message_text('Настройка продуктов', call.from_user.id, call.message.message_id,
                                reply_markup=await product_settings())
