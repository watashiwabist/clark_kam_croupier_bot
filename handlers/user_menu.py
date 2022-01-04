# - *- coding: utf- 8 - *-

from aiogram import types

from config import button_profile, button_help, help_text, chat_text, button_chat, button_coin_game, game_pics, \
    button_dice_game, button_point_game, button_tic_tac_toe_game, \
    button_roulette_game, button_rock_paper_scissors_game, value
from database import db_user_info, db_get_refs, db_get_bot_status
from keyboards.inline.user_key import *
from loader import dp, bot


@dp.message_handler(text=button_profile)
async def user_profile(msg: types.Message):
    bot_status = db_get_bot_status()
    if bot_status == 0:
        await msg.answer('Бот находится на тех. обслуживании.\n\nПожалуйста, попробуйте позже')
        return
    await bot.delete_message(msg.chat.id, msg.message_id)
    user = db_user_info(msg.chat.id)
    bot_info = await bot.get_me()
    bot_username = bot_info.username.replace('_', '\\_')
    ref_cnt = db_get_refs(msg.chat.id)
    if not user:
        await bot.send_message(msg.chat.id, 'Пожалуйста, введите /start')
        return
    try:
        await bot.send_message(msg.chat.id, f'*🧾 Профиль:* {user[1]}\n\n'
                                        f'❕ Ваш id: {user[0]}\n'
                                        f'❕ Дата регистрации - {user[2]}\n'
                                        '➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
                                        f'*💰 Баланс:* {round(user[3], 2)} {value}\n\n'
                                        '➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                        f'Ваша реферальная ссылка:\n'
                                        f't.me/{bot_username}?start={msg.chat.id}\n'
                                        f'👤 Количество рефералов: {ref_cnt}',
                           reply_markup=await profile())
    except Exception as e:
        print(e)


@dp.message_handler(text=button_coin_game)
async def coin_game(msg: types.Message):
    bot_status = db_get_bot_status()
    if bot_status == 0:
        await msg.answer('Бот находится на тех. обслуживании.\n\nПожалуйста, попробуйте позже')
        return
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('coin_game', msg.chat.id))


@dp.message_handler(text=button_dice_game)
async def dice_game(msg: types.Message):
    bot_status = db_get_bot_status()
    if bot_status == 0:
        await msg.answer('Бот находится на тех. обслуживании.\n\nПожалуйста, попробуйте позже')
        return
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('dice_game', msg.chat.id))


@dp.message_handler(text=button_point_game)
async def point_game(msg: types.Message):
    bot_status = db_get_bot_status()
    if bot_status == 0:
        await msg.answer('Бот находится на тех. обслуживании.\n\nПожалуйста, попробуйте позже')
        return
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('point_game', msg.chat.id))


@dp.message_handler(text=button_tic_tac_toe_game)
async def tic_tac_toe_game(msg: types.Message):
    bot_status = db_get_bot_status()
    if bot_status == 0:
        await msg.answer('Бот находится на тех. обслуживании.\n\nПожалуйста, попробуйте позже')
        return
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('tic_tac_toe_game', msg.chat.id))


@dp.message_handler(text=button_rock_paper_scissors_game)
async def rock_paper_scissors_game(msg: types.Message):
    bot_status = db_get_bot_status()
    if bot_status == 0:
        await msg.answer('Бот находится на тех. обслуживании.\n\nПожалуйста, попробуйте позже')
        return
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('rock_paper_scissors_game', msg.chat.id))


@dp.message_handler(text=button_roulette_game)
async def roulette_game(msg: types.Message):
    bot_status = db_get_bot_status()
    if bot_status == 0:
        await msg.answer('Бот находится на тех. обслуживании.\n\nПожалуйста, попробуйте позже')
        return
    photo = open(game_pics[msg.text], 'rb')
    await bot.delete_message(msg.chat.id, msg.message_id)
    await bot.send_photo(msg.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard('roulette_game', msg.chat.id))

@dp.message_handler(text=button_help)
async def user_help(msg: types.Message):
    bot_status = db_get_bot_status()
    if bot_status == 0:
        await msg.answer('Бот находится на тех. обслуживании.\n\nПожалуйста, попробуйте позже')
        return
    await bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer(help_text)


@dp.message_handler(text=button_chat)
async def user_changer(msg: types.Message):
    bot_status = db_get_bot_status()
    if bot_status == 0:
        await msg.answer('Бот находится на тех. обслуживании.\n\nПожалуйста, попробуйте позже')
        return
    await bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer(chat_text, reply_markup=await chat_redirect())
