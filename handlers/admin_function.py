# -*- coding: UTF-8 -*-
from config import cover_img
from database import db_insert_catalog, db_delete_catalog, db_insert_subcatalog, db_delete_subcatalog, \
    db_select_subcatalog, db_insert_product, db_delete_product, db_insert_item, db_insert_client, db_insert_coupon, \
    db_delete_coupon, db_select_item, db_del_item, db_select_all_user, db_insert_history_admin, db_select_history_admin, \
    db_select_product, db_delete_history_admin
from keyboards import catalog, db_select_catalog, subcatalog_list, accept_or_not, cancel, coupon_info, del_items
from loader import dp, bot
from aiogram.types import CallbackQuery

from misc import generate_random_string, coinbase_client
from states import settAdmin, changeCoinbase, transaction, spam
from aiogram import types
from aiogram.dispatcher import FSMContext


####################################################################################################
# CALLBACK HANDLER
####################################################################################################
# -------------------CATALOG-------------------
@dp.callback_query_handler(text='SET_ADD_CATALOG')
async def set_add_catalog(call: CallbackQuery):
    await call.message.answer('Введите название каталога')
    await settAdmin.addCatalog.set()


@dp.callback_query_handler(text='SET_DEL_CATALOG')
async def set_add_catalog(call: CallbackQuery):
    if not db_select_catalog():
        await call.answer('Каталог пуст')
    else:
        await call.message.answer('Выберите удаляемый каталог', reply_markup=await catalog('DEL_CATALOG_',
                                                                                           'BACK_SETTINGS_CATALOG'))


@dp.callback_query_handler(text_startswith='DEL_CATALOG_')
async def set_add_catalog(call: CallbackQuery):
    id_catalog = call.data[12:]
    db_delete_catalog(id_catalog)
    db_delete_subcatalog(id_cat=id_catalog)
    await call.answer('Каталог успешно удален')
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                        reply_markup=await catalog('DEL_CATALOG_', 'BACK_SETTINGS_CATALOG'))


# -------------------/CATALOG-------------------

# -------------------SUBCATALOG-----------------

@dp.callback_query_handler(text='SET_ADD_SUBCATALOG')
async def set_add_subcatalog(call: CallbackQuery):
    if not db_select_catalog():
        await call.answer('Каталог пуст, добавьте для начала каталог')
    else:
        await call.message.answer('Введите название подкаталога')
        await settAdmin.addSubCatalog.set()


@dp.callback_query_handler(text='SET_DEL_SUBCATALOG')
async def set_del_subcatalog(call: CallbackQuery):
    if not db_select_subcatalog():
        await call.answer('Удаляемого подкаталога нет')
    else:
        await bot.edit_message_text('Выберите каталог для выбора под каталога', call.message.chat.id,
                                    call.message.message_id,
                                    reply_markup=await catalog('DEL_SUBCATALOG_IN_', 'BACK_SETTINGS_CATALOG'))


@dp.callback_query_handler(text_startswith='DEL_SUBCATALOG_')
async def set_del_subcatalog(call: CallbackQuery):
    catalog_list = db_select_subcatalog()
    if not catalog_list:
        await call.answer('Данный каталог пуст')
        return
    if call.data.startswith('DEL_SUBCATALOG_IN_'):
        cat_id = call.data[18:]
        await bot.edit_message_text('Выберите удаляемый подкаталог', call.message.chat.id, call.message.message_id,
                                    reply_markup=await subcatalog_list('DEL_SUBCATALOG', cat_id, call.message.chat.id))
    else:
        data = call.data[15:].split('_')
        db_delete_subcatalog(id=data[1])
        if not catalog_list:
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            return
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                            reply_markup=await subcatalog_list('DEL_SUBCATALOG', data[0], call.message.chat.id))
        await call.answer('Подкаталог успешно удален')


@dp.callback_query_handler(text_startswith='ADD_SUBCATALOG_')
async def add_subcatalog_in(call: CallbackQuery):
    data = call.data[15:].split('_')
    db_insert_subcatalog(data[1], data[0])
    await call.message.answer(f'Подкаталог - *{data[0]}* успешно добавлен')


# -------------------/SUBCATALOG-----------------

# -------------------PRODUCT---------------------

@dp.callback_query_handler(text_startswith='SET_ADD_PRODUCT', state='*')
async def set_add_product(call: CallbackQuery, state: FSMContext):
    if call.data.startswith('SET_ADD_PRODUCT_CATALOG_'):
        id_cat = call.data[24:]
        if db_select_subcatalog(id_cat):
            await bot.edit_message_text('Выберите подкаталог', call.message.chat.id, call.message.message_id,
                                        reply_markup=await subcatalog_list('SET_ADD_PRODUCT_SUBCATALOG', id_cat,
                                                                           call.message.chat.id, 'admin'))
        else:
            await call.answer('Каталог пустой')
        return
    elif call.data.startswith('SET_ADD_PRODUCT_SUBCATALOG_'):
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer('*Отлично!*\n\n'
                                  'Теперь вам следует отправить название будущего продукта',
                                  reply_markup=await cancel())
        await state.update_data(subCatID=call.data[27:].split('_')[1])
        await settAdmin.addProductName.set()
    elif db_select_catalog():
        await bot.edit_message_text('Выберите каталог', call.message.chat.id, call.message.message_id,
                                    reply_markup=await catalog('SET_ADD_PRODUCT_CATALOG_', 'BACK_SETTINGS_PRODUCT'))
    else:
        await call.answer('Каталог пуст')


@dp.callback_query_handler(text_startswith='SET_DEl_PRODUCT:')
async def set_del_product(call: CallbackQuery):
    prod_id = call.data[16:]
    db_delete_product(prod_id)
    await call.answer('Продукт успешно удален')
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@dp.callback_query_handler(text_startswith='SET_DATA_PRODUCT:')
async def set_data_product(call: CallbackQuery):
    product_id = call.data[17:]
    data = db_select_item(product_id)
    data_text = ''
    for a in range(len(data)):
        data_text += data[a][2] + '\n'
    await call.message.answer(data_text, reply_markup=await del_items(product_id))


# -------------------/PRODUCT--------------------

# -------------------ITEM------------------------

@dp.callback_query_handler(text_startswith='SET_ADD_ITEM:', state='*')
async def set_add_item(call: CallbackQuery, state: FSMContext):
    prod_id = call.data[13:]
    await call.message.answer('Отправьте *мне данные*\nРазделение данных происходит через *одну пустую* строку\n\n'
                              '*Пример:*\n'
                              'log;pass\n\n'
                              'log;pass', reply_markup=await cancel())
    await state.update_data(product_id=prod_id)
    await settAdmin.addProductData.set()


@dp.callback_query_handler(text_startswith='SET_DEL_ITEM:', state='*')
async def set_del_product(call: CallbackQuery, state: FSMContext):
    await state.update_data(prod_id=call.data[13:])
    await call.message.answer('Напишите удаляемую строчку данных')
    await settAdmin.delItem.set()


# -------------------/ITEM------------------------

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


# -------------------/COUPON----------------------
# @dp.callback_query_handler(text_startswith='STATISTIC')
# async def get_statistic(call: CallbackQuery):
#     try:
#         admin_id = call.data.split(':')[-1]
#         history = db_select_history_admin(admin_id)
#         if history:
#             data = [f'*Данные:* {i[1]}\n*Продано:* Да\n\n' if i[2] else f'*Данные:* {i[1]}\n*Продано:* ' \
#                                                                         f'Нет\n*Подкаталог:* {i[5]}\n\n' for i in
#                     history]
#             data_text = ''
#             for i in data:
#                 data_text += i
#             sold_out_count = len([i for i in history if i[2] == 1])
#             unsold_count = len([i for i in history if i[2] == 0])
#             price = 0
#             for i in history:
#                 if i[2] == 1:
#                     price += float(i[4])
#             data_text += f'*Кол-во проданых/не проданных:* {sold_out_count}/{unsold_count}\n\n' \
#                          f'*Продано на сумму:* {price} $'
#             if len(data_text) > 4096:
#                 for x in range(0, len(data_text), 4096):
#                     print(data_text[x:x + 4096])
#                     await call.message.answer(data_text[x:x + 4096].replace('*', ''))
#             else:
#                 await call.message.answer(data_text)
#         else:
#             await call.answer('Тут пусто :(')
#     except Exception as e:
#         print(f'admin_function.get_statistic: {e}')


####################################################################################################
# MESSAGE HANDLER
####################################################################################################

@dp.message_handler(state=settAdmin.addCatalog)
async def add_catalog(msg: types.Message, state: FSMContext):
    await state.finish()
    db_insert_catalog(msg.text)
    await msg.answer(f'Каталог - *{msg.text}* успешно добавлен')


@dp.message_handler(state=settAdmin.addSubCatalog)
async def add_subcatalog(msg: types.Message, state: FSMContext):
    await msg.answer('В какой каталог добавляем?',
                     reply_markup=await catalog(f'ADD_SUBCATALOG_{msg.text}_', 'BACK_SETTINGS_CATALOG'))
    await state.finish()


@dp.message_handler(state=settAdmin.addProductName)
async def add_product_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer('Теперь вам следует отправить *описание* вашего продукта!', reply_markup=await cancel())
    await settAdmin.next()


@dp.message_handler(state=settAdmin.addProductDescription)
async def add_product_description(msg: types.Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.answer('Какова цена вашего продукта?', reply_markup=await cancel())
    await settAdmin.next()


@dp.message_handler(state=settAdmin.addProductPrice)
async def add_product_price(msg: types.Message, state: FSMContext):
    await state.update_data(price=msg.text)
    await msg.answer('Отправьте обложку продукта, иначе отправьте любой текст', reply_markup=await cancel())
    await settAdmin.next()


@dp.message_handler(content_types=['photo', 'text'], state=settAdmin.addProductImg)
async def add_product_img(msg: types.Message, state: FSMContext):
    if not msg.text:
        await state.update_data(img=msg.photo[0].file_id)
    else:
        await state.update_data(img='None')
    user_data = await state.get_data()
    if user_data['img'] != 'None':
        photo = user_data['img']
    await msg.answer('Укажите цену для работников', reply_markup=await cancel())
    await settAdmin.next()


@dp.message_handler(state=settAdmin.addProductAdminPrice)
async def add_product_admin_price(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        await state.update_data(price_admin=msg.text)
        user_data = await state.get_data()
        photo = open(cover_img, 'rb') if user_data['img'] == 'None' else user_data['img']
        await bot.send_photo(msg.chat.id, photo, f'{user_data["name"]}\n\n'
                                                 f'*Цена:* {user_data["price"]} $\n'
                                                 f'*Описание:* {user_data["description"]}\n\n'
                                                 f'*Оплата за продажу*: {msg.text} $',
                             reply_markup=await accept_or_not())
        photo.close()
    else:
        await msg.answer('Укажите цену для работников', reply_markup=await cancel())


@dp.message_handler(state=settAdmin.addProductData)
async def add_product_data(msg: types.Message, state: FSMContext):
    data = msg.text.split('\n\n')
    user_data = await state.get_data()
    product = db_select_product(id=user_data['product_id'])
    subcatalog = db_select_subcatalog(subcat_id=product[1])
    await state.finish()
    for a in range(len(data)):
        try:
            id_insert = db_insert_item(user_data['product_id'], data[a], msg.chat.id)
            db_insert_history_admin(msg.chat.id, data[a], id_insert, product[7], subcatalog[2])
        except Exception as e:
            print(f'handlers.admin_functions.settAdmin.addProductData: {e}')
            await msg.answer(f'*Произошла ошибка*: {data[a]} - *не была записана*')
    await msg.answer('Данные добавлены')


@dp.message_handler(state=changeCoinbase.token)
async def change_coinbase_token(msg: types.Message, state: FSMContext):
    if ';' not in msg.text:
        await msg.answer('Введите ключ API в формате token;token')
    else:
        data = msg.text.split(';')
        db_insert_client(data)
        await msg.answer('Ключи успешно изменены, проверьте *режим покупки*!')
        await state.finish()


@dp.callback_query_handler(text_startswith='ACCEPT', state='*')
async def accept(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    db_insert_product(user_data['subCatID'], user_data['name'], user_data['description'], user_data['price'],
                      user_data['img'], user_data['price_admin'])
    for a in range(11):
        # noinspection PyBroadException
        try:
            await bot.delete_message(call.message.chat.id, call.message.message_id - a)
        except:
            pass
    await call.message.answer('*SYSTEM:* Продукт успешно создан')
    await state.finish()


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


@dp.message_handler(state=settAdmin.delItem)
async def del_item(msg: types.Message, state: FSMContext):
    data = msg.text
    user_data = await state.get_data()
    prod_id = user_data['prod_id']
    check_item = db_select_item(prod_id, data)
    if check_item:
        db_del_item(check_item[0])
        db_delete_history_admin(check_item[0])
        await msg.answer('Данные успешно удалены')
    else:
        await msg.answer('Данные не найдены, попробуйте еще раз')
    await state.finish()


@dp.message_handler(state=transaction.ltc_address)
async def msg_ltc_address(msg: types.Message, state: FSMContext):
    await state.update_data(ltc_address=msg.text)
    await msg.answer('Оттправьте сумму в $', reply_markup=await cancel())
    await transaction.next()


@dp.message_handler(state=transaction.amount)
async def msg_ltc_amount(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        data = await state.get_data()
        client = await coinbase_client()
        user_id = client.get_accounts()[0]['id']
        try:
            client.send_money(user_id,
                              to=data["ltc_address"],
                              amount=int(msg.text),
                              currency='USD')
        except Exception as e:
            if 'APIError(id=validation_error):' in str(e):
                await msg.answer('Вы ввели не допустимый *Litecoin-адрес*, попробуйте еще раз')
            else:
                await msg.answer('Произошла ошибка, текст ошибки отправил в консоль')
            print(f'handlers.admin_function.msg_ltc_amount: {e}')
        else:
            await msg.answer('Средства успешно отправлены')
        await state.finish()
    else:
        await msg.answer('Оттправьте сумму в $', reply_markup=await cancel())


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
