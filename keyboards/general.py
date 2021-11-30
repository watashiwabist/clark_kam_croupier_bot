from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import db_select_subcatalog, db_select_catalog, db_select_admins, db_select_product, db_select_item


async def cancel():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Отмена', callback_data='CANCEL'))
    return markup


async def subcatalog_list(callback, id, user_id, pos=None):
    subcatalog = db_select_subcatalog(cat_id=id)
    markup = InlineKeyboardMarkup(2)
    key_list = []
    if db_select_admins(user_id):
        markup.add(*[InlineKeyboardButton(sub[2], callback_data=f'{callback}_{id}_{sub[0]}') for sub in subcatalog])
    else:
        for sub in subcatalog:
            for product in db_select_product(sub[0]):
                if len(db_select_item(product[0])) > 0:
                    key_list.append(InlineKeyboardButton(sub[2], callback_data=f'{callback}_{id}_{sub[0]}'))
                    break
        markup.add(*[button for button in key_list])
    if pos == 'user':
        markup.add(InlineKeyboardButton('Назад', callback_data=f'BACK_CATALOG'))
    elif pos == 'admin':
        markup.add(InlineKeyboardButton('Назад', callback_data='SET_ADD_PRODUCT'))
    return markup


async def catalog(callback, back):
    markup = InlineKeyboardMarkup(row_width=2)
    db_catalog = db_select_catalog()
    markup.add(*[InlineKeyboardButton(db_catalog[a][1], callback_data=f'{callback}{db_catalog[a][0]}') for a in
                 range(len(db_catalog))])
    if back is not None:
        markup.add(InlineKeyboardButton('Назад', callback_data=back))
    return markup


async def accept_buy_or(user, prod, subcat_id, cat):
    markup = InlineKeyboardMarkup(row_width=2)
    get_admin = db_select_admins(user)
    if get_admin:
        markup.add(InlineKeyboardButton('🆕 Добавить данные', callback_data=f'SET_ADD_ITEM:{prod}'))
        if get_admin[1] == 2:
            markup.add(InlineKeyboardButton('❌ Удалить', callback_data=f'SET_DEl_PRODUCT:{prod}'),
                       InlineKeyboardButton('ℹ️ Данные', callback_data=f'SET_DATA_PRODUCT:{prod}'))
    button_1 = InlineKeyboardButton('✅ Купить', callback_data=f'GO_BUY:{prod}')
    button_2 = InlineKeyboardButton('↩️ Назад', callback_data=f'BACK_SUBCATALOG_{cat}_{subcat_id}')
    markup.add(button_1, button_2)
    return markup
