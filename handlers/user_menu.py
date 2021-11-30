# - *- coding: utf- 8 - *-

from aiogram import types
from aiogram.types import CallbackQuery

from config import button_profile, button_catalog, catalog_info, button_help, help_text, cover_img, \
    chat_text, button_chat, button_coin_game, game_pics, button_dice_game, button_point_game, button_tic_tac_toe_game, \
    button_roulette_game, button_rock_paper_scissors_game
from database import db_user_info, db_select_catalog, db_get_refs
from keyboards import catalog
from keyboards.inline.user_key import *
from loader import dp, bot


@dp.message_handler(text=button_profile)
async def user_profile(msg: types.Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    user = db_user_info(msg.chat.id)
    bot_username = await bot.get_me()
    ref_cnt = db_get_refs(msg.chat.id)
    if not user:
        await bot.send_message(msg.chat.id, 'Пожалуйста, введите /start')
        return
    await bot.send_message(msg.chat.id, f'*🧾 Профиль:* {user[1]}\n\n'
                                        f'❕ Ваш id: {user[0]}\n'
                                        f'❕ Дата регистрации - {user[2]}\n'
                                        '➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
                                        f'*💰 Баланс:* {user[3]} {value}\n\n'
                                        '➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                        f'Ваша реферальная ссылка:\n'
                                        f't.me/{bot_username.username}?start={msg.chat.id}\n'
                                        f'💵 Заработано: 0.00 {value}\n'
                                        f'👤 Количество рефералов: {ref_cnt}',
                           reply_markup=await profile())


@dp.message_handler(text=button_coin_game)
async def coin_game(msg: types.Message):
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('coin_game'))

@dp.message_handler(text=button_dice_game)
async def coin_game(msg: types.Message):
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('dice_game'))

@dp.message_handler(text=button_point_game)
async def coin_game(msg: types.Message):
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('point_game'))

@dp.message_handler(text=button_tic_tac_toe_game)
async def coin_game(msg: types.Message):
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('tic_tac_toe_game'))

@dp.message_handler(text=button_rock_paper_scissors_game)
async def coin_game(msg: types.Message):
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('rock_paper_scissors_game'))

@dp.message_handler(text=button_roulette_game)
async def coin_game(msg: types.Message):
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('roulette_game'))




# @dp.message_handler(text=button_catalog)
# async def user_catalog(msg: types.Message):
#     await bot.delete_message(msg.chat.id, msg.message_id)
#     if not db_select_catalog():
#         await msg.answer('Каталог пуст')
#     else:
#         await bot.send_photo(msg.chat.id, open(cover_img, 'rb'), catalog_info,
#                              reply_markup=await catalog('ID_CATALOG_', None))


# @dp.message_handler(text=button_help)
# async def user_help(msg: types.Message):
#     check_help_img = os.path.exists(help_url)
#     await bot.delete_message(msg.chat.id, msg.message_id)
#     if check_help_img:
#         help_img = open(help_url, 'rb')
#         await bot.send_photo(msg.chat.id, photo=help_img, caption=help_text)
#     else:
#         await msg.answer(help_text)

@dp.message_handler(text=button_help)
async def user_help(msg: types.Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer(help_text)


@dp.message_handler(text=button_chat)
async def user_changer(msg: types.Message):
    await bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer(chat_text, reply_markup=await chat_redirect())


# @dp.callback_query_handler(text_startswith='BACK_CATALOG')
# async def user_view_pos(call: CallbackQuery):
#     if not db_select_catalog():
#         await call.answer('Каталог пуст')
#     else:
#         await bot.edit_message_caption(call.message.chat.id, call.message.message_id, caption=catalog_info,
#                                        reply_markup=await catalog('ID_CATALOG_', None))
