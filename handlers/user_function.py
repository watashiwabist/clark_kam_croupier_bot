# -*- coding: UTF-8 -*-
import datetime
import random
from operator import itemgetter

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from config import value, game_names, game_pics2, rps, gifs, roulette_caption, deck, ttt_win, secret_word, merchant_id, \
    min_top_up
from database import db_user_info, \
    db_user_insert, db_user_update, db_delete_coupon, db_get_user_balance, db_create_game_lobby, db_get_game_history, \
    db_get_user_name, db_delete_lobby, db_get_game_name, \
    db_check_game_available, db_get_player_id, db_get_lobby_bet, db_join_lobby, db_set_lobby_status, db_get_lobby_info, \
    db_set_player_choice, db_set_winner, db_get_fee, db_set_deck, db_insert_bill, db_get_bill, db_change_status, \
    db_get_all_games_stat
from free_kassa import create_order, bill_info, get_balance, withdraw_order, available_payments
from keyboards import profile, cancel, db_select_coupon, deposit, game_keyboard, lobby_info, lobby_owner, RPS_game, \
    coin_game_markup, spin_the_roulette, point_choice, ttt_table, payment_info, withdraw_markup, \
    freekassa_payment_markup
from loader import dp, bot
from misc.misc import count_players, sleep, create_qiwi_bill, qiwi_bill_info, pay_qiwi, \
    get_payment_comment
from states import settUser, Game, withdraw


# CALLBACK HANDLER

@dp.callback_query_handler(text_startswith='COUPON')
async def user_activate_coupon(call: CallbackQuery):
    await call.message.answer('Введите купон:')
    await settUser.coupon.set()


@dp.callback_query_handler(text_startswith='BACK_PROFILE')
async def user_view_order(call: CallbackQuery):
    user = db_user_info(call.message.chat.id)
    bot_username = await bot.get_me()
    if not user:
        await bot.send_message(call.message.chat.id, 'Пожалуйста, введите /start')
        return
    await bot.edit_message_text(call.message.chat.id, f'*🧾 Профиль:* {user[1]}\n\n'
                                                      f'❕ Ваш id: {user[0]}\n'
                                                      f'❕ Дата регистрации - {user[2]}\n'
                                                      '➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
                                                      f'*💰 Баланс:* {user[4]} {value}\n\n'
                                                      '➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                                      f'Ваша реферальная ссылка:\n'
                                                      f't.me/{bot_username.username}?start={call.message.chat.id}\n'
                                                      f'👤 Количество рефералов: 0',
                                reply_markup=await profile())


@dp.callback_query_handler(text_startswith='TOPUP_')
async def user_top_up(call: CallbackQuery, state: FSMContext):
    merchant = call.data.removeprefix('TOPUP_')
    await call.message.answer(
        f'Отправьте сумму для пополнения в *{value}*\n\nМинимальная сумма пополнения {min_top_up}{value}',
        reply_markup=await cancel())
    await state.update_data(merchant=merchant)
    await settUser.topUp.set()


# MESSAGE HANDLER
@dp.message_handler(state=settUser.topUp)
async def make_topup(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer(f'Отправьте сумму для пополнения в *{value}*', reply_markup=await cancel())
        return
    sum = int(msg.text)
    if sum < min_top_up:
        await msg.answer(f'Минимальная сумма пополнения {min_top_up} *{value}*', reply_markup=await cancel())
        return
    data = await state.get_data()
    merchant = data['merchant']
    await state.update_data(amount=sum)
    await state.finish()
    if merchant == 'qiwi':
        try:
            bill = await create_qiwi_bill(sum)
            db_insert_bill(bill.bill_id, msg.chat.id, sum, bill.creation, comment=bill.comment)
            await msg.answer(f'*Сумма:* `{sum} {value}`\n\n'
                             f'*Для оплаты нажмите на кнопку* - `Оплатить`\n\n'
                             f'*После оплаты нажмите на кнопку* - `Проверить оплату`\n\n',
                             parse_mode='Markdown',
                             reply_markup=await payment_info(merchant, bill.pay_url, bill.bill_id))
        except Exception as e:
            print(f'qiwi merchant: {e}')
    elif merchant == 'freekassa':
        order_id = await get_payment_comment()
        bill = create_order(sum, secret_word, merchant_id, order_id)
        db_insert_bill(bill['id'], msg.chat.id, sum, str(datetime.datetime.now()), comment=bill['id'])
        await msg.answer(f'*Сумма:* `{sum} {value}`\n\n'
                         f'*Для оплаты нажмите на кнопку* - `Оплатить`\n\n'
                         f'*После оплаты нажмите на кнопку* - `Проверить оплату`\n\n',
                         parse_mode='Markdown',
                         reply_markup=await payment_info(merchant, bill['url'], bill['id']))


@dp.message_handler(state=settUser.coupon)
async def activate_coupon(msg: types.Message, state: FSMContext):
    coup = db_select_coupon(text=msg.text)
    if coup is None:
        await msg.answer('Купон не верный')
    else:
        db_user_insert(user=msg.chat.id, amount=coup[2])
        db_delete_coupon(coup[0])
        await msg.answer('Купон активирован')
    await state.finish()


@dp.callback_query_handler(text='WITHDRAW')
async def choosewithdraw(call: CallbackQuery):
    await call.message.answer('Выберите куда хотите вывести деньги', reply_markup=await withdraw_markup())


@dp.callback_query_handler(text='PAYMENT_FREEKASSA')
async def choosepaymentwithdraw(call: CallbackQuery):
    await call.message.answer('Выберите куда хотите вывести деньги', reply_markup=await freekassa_payment_markup())


@dp.callback_query_handler(text_startswith='WITHDRAW_')
async def withdraw_amount(call: CallbackQuery, state: FSMContext):
    merchant = call.data.removeprefix('WITHDRAW_')
    await state.update_data(merchant=merchant)
    await withdraw.amount.set()
    balance = db_get_user_balance(call.message.chat.id)
    await call.message.answer(f'Введите сумму на вывод от {min_top_up}р. Ваш баланс: {round(balance, 2)} {value}')


@dp.message_handler(state=withdraw.amount)
async def withdraw_amont(msg: types.Message, state: FSMContext):
    balance = int(db_get_user_balance(msg.chat.id))
    if not msg.text.isdigit() or balance < int(msg.text) or int(msg.text) < min_top_up:
        await msg.answer(f'Введите сумму на вывод от {min_top_up}р. Ваш баланс: {round(balance, 2)} {value}',
                         reply_markup=await cancel())
        return
    await state.update_data(amount=int(msg.text))
    await msg.answer('Введите номер счета для вывода')
    await withdraw.account.set()


@dp.message_handler(state=withdraw.account)
async def withdraw_acc(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    amount = int(data['amount'])
    merchant = data['merchant']
    await state.finish()
    if merchant == 'qiwi':
        if await pay_qiwi(amount, msg.text):
            db_user_update(amount, msg.chat.id)
            await msg.answer('Деньги были успешно отправлены на ваш счет.')
        else:
            await msg.answer('Произошла ошибка перевода.\n\nПопробуйте еще раз позже.')
    elif 'freekassa' in merchant:
        wallet_balance = get_balance()
        if float(wallet_balance['balance'][0]['value']) < amount:
            await msg.answer('Произошла ошибка перевода.\n\nПопробуйе еще раз позже или обратитесь в администрацию.')
            return
        available_currency = available_payments()
        choosen_payment = merchant.split('_')[1]
        for payment in available_currency['currencies']:
            if choosen_payment == payment['name']:
                # if amount > payment['can_exchange']:
                #     await msg.answer(
                #         'Произошла ошибка перевода.\n\nПопробуйте еще раз позже или обратитесь в администрацию.')
                #     return
                status = withdraw_order(amount, msg.text, payment['id'])
                if status['type'] != 'success':
                    await msg.answer('Кажется произошла ошибка.\nПопробуйте позже.')
                    return
                await msg.answer('Деньги были успешно отправлены на ваш счет.')
                return
        await msg.answer('Выбранный способ вывода не доступен в данный момент')


@dp.callback_query_handler(text_startswith='STATUS_PAY_')
async def user_full_stat(call: CallbackQuery):
    merchant, bill_id = call.data.replace('STATUS_PAY_', '').split('_')
    db_info = db_get_bill(bill_id, call.message.chat.id)
    if db_info[4] != 'progress':
        return
    if merchant == 'qiwi':
        info = await qiwi_bill_info(bill_id)
        status = info.status
        if status == 'WAITING':
            await call.message.answer("Платеж не найден")
            return
        elif status == 'EXPIRED':
            db_change_status(bill_id, status=status.lower())
            await call.message.answer("Время жизни оплаты истекло.\nСоздайте новый счет на оплату.")
            return
        elif status == 'REJECTED':
            db_change_status(bill_id, status=status.lower())
            await call.message.answer("Произошла ошибка оплаты заказа.\nСоздайте новый счет на оплату.")
        elif status == 'PAID':
            db_user_insert(call.message.chat.id, info.amount)
            db_change_status(bill_id)
            await call.message.answer(f'Баланс успешно пополнен на {info.amount} {value}')
            await ref_percent(call.message.chat.id, info.amount)
    elif merchant == 'freekassa':
        info = bill_info(bill_id)
        if len(info['orders']) == 0:
            await call.message.answer("Платеж не найден")
            return
        else:
            for order in info['orders']:
                if order['status'] == 1:
                    db_user_insert(call.message.chat.id, order['amount'])
                    db_change_status(bill_id)
                    await call.message.answer(f'Баланс успешно пополнен на {order["amount"]} {value}')
                    await ref_percent(call.message.chat.id, order['amount'])
                    return
            await call.message.answer('Платеж не найден')


async def ref_percent(user_id, amount):
    user = db_user_info(user_id)
    percent = (amount * 35) / 100
    if user[4] is not None and user[4] != 0:
        await bot.send_message(user[4], f'Ваш реферал пополнил баланс.\nВам начислено {percent} {value}')
        db_user_insert(user[4], percent)


@dp.callback_query_handler(text_startswith='STATISTICS_')
async def user_full_stat(call: CallbackQuery):
    game_name = call.data.replace('STATISTICS_', '')
    all_games = db_get_all_games_stat(game_name)
    game_income = {}
    game_loose = {}
    for game in all_games:
        looser = game[3] if game[9] != game[3] else game[4]
        if game[9] != 0 and game[9] not in game_income:
            game_income[game[9]] = 0
        if looser not in game_income:
            game_income[looser] = 0
        if game[8] == 'done' and game[9] != 0:
            if looser not in game_loose:
                game_loose[looser] = 0
            game_income.update({game[9]: game_income[game[9]] + game[2]})
            game_loose.update({looser: game_loose[looser] + game[2]})
    game_count = len(db_get_game_history(call.message.chat.id, game_name))
    income_sorted = list(reversed(sorted(game_income.items(), key=itemgetter(1))))
    cur_user_place = len(income_sorted)
    for i in range(len(income_sorted)):
        if call.message.chat.id in income_sorted[i]:
            cur_user_place = i + 1
            break

    top_str = ''
    for i in range(len(income_sorted)):
        if i == 0:
            top_str += f'🥇 1 место - {db_get_user_name(income_sorted[0][0])} - {round(income_sorted[0][1], 2)} {value}\n'
        elif i == 1:
            top_str += f'🥈 2 место - {db_get_user_name(income_sorted[1][0])} - {round(income_sorted[1][1], 2)} {value}\n'
        elif i == 2:
            top_str += f'🥉 3 место - {db_get_user_name(income_sorted[2][0])} - {round(income_sorted[2][1], 2)} {value}\n'
        elif i > 2:
            break

    if game_count == 0:
        game_loose[call.message.chat.id] = 0
        game_income[call.message.chat.id] = 0
    await call.message.answer(f'🏆 ТОП 3 игроков:\n\n'
                              f'{top_str}\n'
                              f'✨ Ваше место в рейтинге {cur_user_place} из {len(game_income)} ({round(game_income[call.message.chat.id], 2)} {value})\n\n'
                              f'⚜️ Кол-во игр: {game_count}\n'
                              f'⚜️ Выиграно: {round(game_income[call.message.chat.id], 2)} {value}\n'
                              f'⚜️ Проиграно: {round(game_loose[call.message.chat.id], 2)} {value}')


@dp.callback_query_handler(text_startswith='REFRESH_')
async def user_full_stat(call: CallbackQuery):
    game = call.data.replace('REFRESH_', '')
    photo = open(game_pics2[game], 'rb')
    await bot.send_photo(call.message.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard(game, call.message.chat.id))


def poop(record):
    return record[0]


@dp.callback_query_handler(text_startswith='MY_GAMES_')
async def user_game_stat(call: CallbackQuery):
    game = call.data.replace('MY_GAMES_', '')
    history = sorted(db_get_game_history(call.message.chat.id, game), key=poop, reverse=True)
    cur_game_name = game_names[game]
    str = ''
    for i in history:
        if i[9] is None:
            status = 'в процессе'
        elif i[9] is not None and i[9] == call.message.chat.id:
            status = 'победа'
        else:
            status = 'поражение'
        str += f'№{i[0]} | {cur_game_name} | {status} | ставка: {i[2]}\n'
    await call.message.answer(f'*Мои игры:*\n\n' + str)


@dp.callback_query_handler(text_startswith='CREATE_GAME_')
async def user_create_game(call: CallbackQuery, state: FSMContext):
    game = call.data.replace('CREATE_GAME_', '')
    try:
        balance = db_get_user_balance(call.message.chat.id)
        msg = await bot.send_message(call.message.chat.id, f'Ваш баланс: {round(balance, 2)} {value}. Введите ставку:',
                                     reply_markup=await cancel())
        await state.update_data(game=game, balance=balance, msg=msg)
        await Game.create_lobby.set()
    except Exception as e:
        await call.answer('Произошла ошибка, попробуйте прописать /start')
        print(f'handlers.user_function.user_create_game: {e}')


@dp.callback_query_handler(text_startswith='NOPLAY_')
async def dont_play_game(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    game = call.data.replace('NOPLAY_', '')
    photo = open(game_pics2[game], 'rb')
    await bot.send_photo(call.message.chat.id, photo,
                         '♻️ Доступные игры:\n'
                         'Или найди оппонента в чате', reply_markup=await game_keyboard(game, call.message.chat.id))


@dp.callback_query_handler(text_startswith='DELETE_')
async def delete_lobby(call: CallbackQuery):
    lobby_id = int(call.data.replace('DELETE_', ''))
    bet = db_get_lobby_bet(lobby_id)
    db_delete_lobby(lobby_id)
    db_user_insert(call.message.chat.id, bet)
    await call.message.answer(f'Игра №{lobby_id} удалена!')


@dp.callback_query_handler(text_startswith='PLAY_')
async def play_game(call: CallbackQuery):
    lobby_id = int(call.data.replace('PLAY_', ''))
    availvable = db_check_game_available(lobby_id)
    if availvable != 'active':
        await call.message.answer(f'Кажется данное лобби уже не существует.\n'
                                  f'Попробуйте вступить в другую игру.')
        return
    user_balance = db_get_user_balance(call.message.chat.id)
    game_bet = db_get_lobby_bet(lobby_id)
    if user_balance < game_bet:
        await call.message.answer('У вас не достаточно денег на балансе')
        return
    lobby_info = db_get_lobby_info(lobby_id)
    if call.message.chat.id in lobby_info:
        await call.message.answer('Вы уже в игре!')
        return
    db_user_update(game_bet, call.message.chat.id)
    game_name = db_get_game_name(lobby_id)
    fee = db_get_fee()
    players_count = count_players(lobby_info)
    db_join_lobby(lobby_id, call.message.chat.id, players_count + 1)
    if game_name != 'roulette_game':
        db_set_lobby_status(lobby_id, 'progress')
        player_1 = db_get_player_id(lobby_id, 1)
        player_2 = db_get_player_id(lobby_id, 2)
        await bot.send_message(player_1, f'Игра начнется, через 5 секунд')
        await bot.send_message(player_2, f'Игра начнется, через 5 секунд')
        await sleep(4)
    if game_name == 'rock_paper_scissors_game':
        db_set_lobby_status(lobby_id, 'progress')
        await bot.send_message(player_1, f'Выберите вариант:', reply_markup=await RPS_game(lobby_id, 1))
        await bot.send_message(player_2, f'Выберите вариант:', reply_markup=await RPS_game(lobby_id, 2))
    elif game_name == 'dice_game':
        db_set_lobby_status(lobby_id, 'done')
        await bot.send_message(player_1, 'Ваш кубик 👇')
        await bot.send_message(player_2, 'Ваш кубик 👇')
        dice1 = await bot.send_dice(player_1)
        dice2 = await bot.send_dice(player_2)
        await bot.send_message(player_1, 'Кубик соперника 👇')
        await bot.forward_message(player_1, dice2.chat.id, dice2.message_id)
        await bot.send_message(player_2, 'Кубик соперника 👇')
        await bot.forward_message(player_2, dice1.chat.id, dice1.message_id)
        win_sum = game_bet * 2 - ((game_bet * 2) * (fee / 100))
        if dice1.dice.value == dice2.dice.value:
            await bot.send_message(player_1, 'Ничья! Деньги возвращены на баланс')
            await bot.send_message(player_2, 'Ничья! Деньги возвращены на баланс')
            db_user_insert(player_1, game_bet)
            db_user_insert(player_2, game_bet)
            db_set_winner(lobby_id, 0)
            return
        elif dice1.dice.value < dice2.dice.value:
            player_1, player_2 = player_2, player_1
        await bot.send_message(player_1, f'Победа! Выигрыш составляет {win_sum} {value}')
        await bot.send_message(player_2, 'К сожалению вы проиграли 😔')
        db_user_insert(player_1, win_sum)
        db_set_winner(lobby_id, player_1)
    elif game_name == 'coin_game':
        db_set_lobby_status(lobby_id, 'progress')
        await bot.send_message(player_1, f'Выберите сторону:', reply_markup=await coin_game_markup(lobby_id, 1))
        await bot.send_message(player_2, f'Выберите сторону:', reply_markup=await coin_game_markup(lobby_id, 2))
    elif game_name == 'roulette_game':
        new_lobby_info = db_get_lobby_info(lobby_id)
        new_player_count = count_players(new_lobby_info)
        if new_player_count == 5:
            ...  # start
        user_name_list = [db_get_user_name(user) for user in new_lobby_info[3:3 + new_player_count]]
        roulette_text = roulette_caption
        for i in range(len(user_name_list)):
            roulette_text = roulette_text.replace(f'{i + 1} (Свободное место)', f'{i + 1} 🔷 {user_name_list[i]}')
        await bot.send_message(new_lobby_info[3], roulette_text, reply_markup=await spin_the_roulette(lobby_id))
        await bot.send_message(call.message.chat.id, roulette_text.replace('Добавился новый игрок:\n\n', ''))
    elif game_name == 'point_game':
        current_deck = deck
        random.shuffle(current_deck)
        player_1_point = 0
        player_2_point = 0
        player_1_point += current_deck.pop()
        player_2_point += current_deck.pop()
        player_1_point += current_deck.pop()
        player_2_point += current_deck.pop()

        db_set_player_choice(lobby_id, 1, player_1_point)
        db_set_player_choice(lobby_id, 2, player_2_point)
        db_set_deck(lobby_id, ','.join(map(str, current_deck)))
        await bot.send_message(lobby_info[3], f'У вас {player_1_point} очков',
                               reply_markup=await point_choice(lobby_id, 1))
        await bot.send_message(call.message.chat.id, f'У вас {player_2_point} очков',
                               reply_markup=await point_choice(lobby_id, 2))
    elif game_name == 'tic_tac_toe_game':
        new_lobby_info = db_get_lobby_info(lobby_id)
        first = random.choice([0, 1])
        db_set_player_choice(lobby_id, 3, first)
        db_set_player_choice(lobby_id, 1, first)
        first_msg = await bot.send_message(new_lobby_info[3 + first], f'🟢 Ваш ход!\n\nВаш знак ❌',
                                           reply_markup=await ttt_table(lobby_id, first))
        second_msg = await bot.send_message(new_lobby_info[3 + ((first + 1) % 2)], f'🔴 Ход противника!\n\nВаш знак ⭕️',
                                            reply_markup=await ttt_table(lobby_id, (first + 1) % 2))
        together = str(first_msg.message_id) + str(second_msg.message_id)
        db_set_winner(lobby_id, together)


@dp.callback_query_handler(text_startswith='LOBBY_')
async def show_lobby_info(call: CallbackQuery):
    info = call.data.removeprefix('LOBBY_').split('-')
    user_name = db_get_user_name(int(info[3]))
    await bot.send_message(call.message.chat.id,
                           f'{game_names[info[1]]}, игра № {info[0]}\n'
                           f'Ставка: {info[2]} {value}\n\n'
                           f'Создал: {user_name}', reply_markup=await lobby_info(info[0], info[1])
        if call.message.chat.id != int(info[3])
        else await lobby_owner(info[0]))


@dp.message_handler(state=Game.create_lobby)
async def user_create_lobby(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer('Отправьте сумму для ставки', reply_markup=await cancel())
        return
    cur_bet = float(msg.text)
    data = await state.get_data()
    balance = float(data['balance'])
    game = data['game']
    if balance < cur_bet or cur_bet <= 10.:
        await msg.answer(f'Недостаточно средств. Минимальная ставка 10 {value}', reply_markup=await deposit())
        return
    await state.finish()
    await bot.delete_message(msg.chat.id, data['msg'].message_id)
    game_id = db_create_game_lobby(msg.chat.id, cur_bet, game)
    await msg.answer(f'Игра №{game_id} создана, ожидание соперника')
    db_user_update(cur_bet, msg.chat.id)


@dp.callback_query_handler(text_startswith='RPS_')
async def RPS_results(call: CallbackQuery):
    call_info = call.data.removeprefix('RPS_').split('_')
    db_set_player_choice(call_info[1], int(call_info[2]), rps[call_info[0]])
    fee = db_get_fee()
    lobby_info = db_get_lobby_info(call_info[1])
    if lobby_info[8] == 'done':
        return
    if lobby_info[5] is None:
        await bot.send_message(lobby_info[4], 'Ожидаем хода противника')
    elif lobby_info[6] is None:
        await bot.send_message(lobby_info[3], 'Ожидаем хода противника')
    else:
        win_sum = lobby_info[2] * 2 - ((lobby_info[2] * 2) * (fee / 100))
        player_1_choice = lobby_info[5]
        player_2_choice = lobby_info[6]
        db_set_lobby_status(lobby_info[0], 'done')
        if player_1_choice == 1:
            if player_2_choice == 1:
                await bot.send_message(lobby_info[3], 'Ничья! Деньги возвращены на баланс')
                await bot.send_message(lobby_info[4], 'Ничья! Деньги возвращены на баланс')
                db_user_insert(lobby_info[3], lobby_info[2])
                db_user_insert(lobby_info[4], lobby_info[2])
                db_set_winner(lobby_info[0], 0)
            elif player_2_choice == 2:
                await bot.send_message(lobby_info[3],
                                       f'Вы победили! +{win_sum} {value}')
                await bot.send_message(lobby_info[4], 'Вы проиграли!')
                db_user_insert(lobby_info[3], win_sum)
                db_set_winner(lobby_info[0], lobby_info[3])  # p1 win
            else:
                await bot.send_message(lobby_info[4],
                                       f'Вы победили! +{win_sum} {value}')
                await bot.send_message(lobby_info[3], 'Вы проиграли!')
                db_user_insert(lobby_info[4], win_sum)
                db_set_winner(lobby_info[0], lobby_info[4])  # p2 win
        elif player_1_choice == 2:
            if player_2_choice == 1:
                await bot.send_message(lobby_info[4],
                                       f'Вы победили! +{win_sum} {value}')
                await bot.send_message(lobby_info[3], 'Вы проиграли!')
                db_user_insert(lobby_info[4], win_sum)
                db_set_winner(lobby_info[0], lobby_info[4])  # p2 win
            elif player_2_choice == 2:
                await bot.send_message(lobby_info[3], 'Ничья! Деньги возвращены на баланс')
                await bot.send_message(lobby_info[4], 'Ничья! Деньги возвращены на баланс')
                db_user_insert(lobby_info[3], lobby_info[2])
                db_user_insert(lobby_info[4], lobby_info[2])
                db_set_winner(lobby_info[0], 0)  # draw
            else:
                await bot.send_message(lobby_info[3],
                                       f'Вы победили! +{win_sum} {value}')
                await bot.send_message(lobby_info[4], 'Вы проиграли!')
                db_user_insert(lobby_info[3], win_sum)
                db_set_winner(lobby_info[0], lobby_info[3])  # p1 win
        else:
            if player_2_choice == 1:
                await bot.send_message(lobby_info[3],
                                       f'Вы победили! +{win_sum} {value}')
                await bot.send_message(lobby_info[4], 'Вы проиграли!')
                db_user_insert(lobby_info[3], win_sum)
                db_set_winner(lobby_info[0], lobby_info[3])  # p1 win
            elif player_2_choice == 2:
                await bot.send_message(lobby_info[4],
                                       f'Вы победили! +{win_sum} {value}')
                await bot.send_message(lobby_info[3], 'Вы проиграли!')
                db_user_insert(lobby_info[4], win_sum)
                db_set_winner(lobby_info[0], lobby_info[4])  # p2 win
            else:
                await bot.send_message(lobby_info[3], 'Ничья! Деньги возвращены на баланс')
                await bot.send_message(lobby_info[4], 'Ничья! Деньги возвращены на баланс')
                db_user_insert(lobby_info[3], lobby_info[2])
                db_user_insert(lobby_info[4], lobby_info[2])
                db_set_winner(lobby_info[0], 0)  # draw


@dp.callback_query_handler(text_startswith='COIN_CHOOSE_')
async def coin_results(call: CallbackQuery):
    call_info = call.data.replace('COIN_CHOOSE_', '').split('_')
    call_info[1] = int(call_info[1])
    call_info[2] = int(call_info[2])
    lobby_info = db_get_lobby_info(call_info[1])
    if lobby_info[6] is not None or lobby_info[5] is not None or lobby_info[8] == 'done':
        return
    db_set_player_choice(call_info[1], call_info[2], 1 if call_info[0] == 'eagle' else 0)
    fee = db_get_fee()
    win_sum = lobby_info[2] * 2 - ((lobby_info[2] * 2) * (fee / 100))
    await bot.send_message(lobby_info[4 - (call_info[2] + 1) % 2],
                           'Вам достался Орел' if call_info[0] != 'eagle' else 'Вам досталась Решка')
    await bot.send_message(lobby_info[2 + call_info[2]],
                           'Вы выбрали Орел' if call_info[0] == 'eagle' else 'Вы выбрали Решку')
    side = random.choice([0, 1])  # 0 - Орел, 1 - Решка
    await bot.send_video(lobby_info[4], open(gifs[side], 'rb'), caption='Выпал Орел' if side == 0 else 'Выпала Решка')
    await bot.send_video(lobby_info[3], open(gifs[side], 'rb'), caption='Выпал Орел' if side == 0 else 'Выпала Решка')
    db_set_lobby_status(lobby_info[0], 'done')
    if side == 0:
        if call_info[0] == 'eagle':
            await bot.send_message(lobby_info[2 + call_info[2]], f'Ура! Вы выиграли {win_sum} {value}')
            await bot.send_message(lobby_info[4 - (call_info[2] + 1) % 2], 'К сожалению вы проиграли 😔')
            db_user_insert(lobby_info[2 + call_info[2]], win_sum)
            db_set_winner(lobby_info[0], lobby_info[2 + call_info[2]])
        else:
            await bot.send_message(lobby_info[2 + call_info[2]], 'К сожалению вы проиграли 😔')
            await bot.send_message(lobby_info[4 - (call_info[2] + 1) % 2], f'Ура! Вы выиграли {win_sum} {value}')
            db_user_insert(lobby_info[4 - (call_info[2] + 1) % 2], win_sum)
            db_set_winner(lobby_info[0], lobby_info[4 - (call_info[2] + 1) % 2])
    else:
        if call_info[0] == 'eagle':
            await bot.send_message(lobby_info[2 + call_info[2]], 'К сожалению вы проиграли 😔')
            await bot.send_message(lobby_info[4 - (call_info[2] + 1) % 2], f'Ура! Вы выиграли {win_sum} {value}')
            db_user_insert(lobby_info[4 - (call_info[2] + 1) % 2], win_sum)
            db_set_winner(lobby_info[0], lobby_info[4 - (call_info[2] + 1) % 2])
        else:
            await bot.send_message(lobby_info[2 + call_info[2]], f'Ура! Вы выиграли {win_sum} {value}')
            await bot.send_message(lobby_info[4 - (call_info[2] + 1) % 2], 'К сожалению вы проиграли 😔')
            db_user_insert(lobby_info[2 + call_info[2]], win_sum)
            db_set_winner(lobby_info[0], lobby_info[2 + call_info[2]])


@dp.callback_query_handler(text_startswith='SPIN_')
async def spin_game(call: CallbackQuery):
    lobby_id = int(call.data.replace('SPIN_', ''))
    lobby_info = db_get_lobby_info(lobby_id)
    if lobby_info[8] == 'done':
        return
    player_cnt = count_players(lobby_info)
    user_name_list = [db_get_user_name(user) for user in lobby_info[3:3 + player_cnt]]
    roulette_text = roulette_caption.replace('Добавился новый игрок:\n\n', '')
    fee = db_get_fee()
    win_sum = lobby_info[2] * 2 - ((lobby_info[2] * 2) * (fee / 100))
    for i in range(len(user_name_list)):
        roulette_text = roulette_text.replace(f'{i + 1} (Свободное место)', f'{i + 1} 🔷 {user_name_list[i]}')
    if player_cnt != 5:
        roulette_text = roulette_text[:-22 * (5 - player_cnt)]
    [await bot.send_message(user, f'Игра в Рулетку №{lobby_id} начнется через 5 секунд!\n\n' + roulette_text) for user
     in lobby_info[3:3 + player_cnt]]
    await sleep(4)
    winner = random.choice(range(player_cnt))
    for user in lobby_info[3:3 + player_cnt]:
        winner_text = ''
        if user == lobby_info[3 + winner]:
            winner_text = f'\n\nВы выиграли: {win_sum} {value}'
        await bot.send_message(user, f'Игра №{lobby_id}\n\n'
                                     f'Победил игрок: {user_name_list[winner]}'
                                     f'{winner_text}')
    db_user_insert(lobby_info[3 + winner], win_sum)
    db_set_winner(lobby_info[0], lobby_info[3 + winner])
    db_set_lobby_status(lobby_info[0], 'done')


@dp.callback_query_handler(text_startswith='TAKE_')
async def take_card(call: CallbackQuery):
    call_info = call.data.replace('TAKE_', '').split('_')
    call_info[0] = int(call_info[0])
    call_info[1] = int(call_info[1])
    lobby_info = db_get_lobby_info(call_info[0])
    if lobby_info[4 + call_info[1]] >= 21 or lobby_info[7] == call_info[1] or lobby_info[8] == 'done':
        return
    current_deck = list(map(int, lobby_info[8].split(',')))
    point = current_deck.pop()
    curr_points = lobby_info[4 + call_info[1]] + point
    db_set_player_choice(lobby_info[0], call_info[1], curr_points)
    db_set_deck(lobby_info[0], ','.join(map(str, current_deck)))
    if curr_points < 21:
        await bot.send_message(lobby_info[2 + call_info[1]], f'Сумма карт {curr_points}, ждем противника',
                               reply_markup=await point_choice(call_info[0],
                                                               call_info[1]))
    else:
        other_player = call_info[1] % 2 + 1
        await bot.send_message(lobby_info[2 + call_info[1]], f'Сумма карт {curr_points}, ждем противника')
        if lobby_info[7] is not None or lobby_info[4 + other_player] >= 21:
            await point_results(call_info[0])


@dp.callback_query_handler(text_startswith='YETER_')
async def point_yeter(call: CallbackQuery):
    call_info = call.data.replace('YETER_', '').split('_')
    call_info[0] = int(call_info[0])
    call_info[1] = int(call_info[1])
    lobby_info = db_get_lobby_info(call_info[0])
    if lobby_info[8] == 'done':
        return
    other_player = call_info[1] % 2 + 1
    if lobby_info[7] is not None or lobby_info[4 + other_player] >= 21:
        await point_results(call_info[0])
    else:
        db_set_player_choice(lobby_info[0], 3, call_info[1])


async def point_results(lobby_id):
    lobby_info = db_get_lobby_info(lobby_id)
    fee = db_get_fee()
    db_set_lobby_status(lobby_id, 'done')
    win_sum = lobby_info[2] * 2 - ((lobby_info[2] * 2) * (fee / 100))
    player_1_points = lobby_info[5]
    player_2_points = lobby_info[6]
    if player_1_points == player_2_points:
        await bot.send_message(lobby_info[3], 'Ничья! Деньги возвращены на баланс')
        await bot.send_message(lobby_info[4], 'Ничья! Деньги возвращены на баланс')
        db_user_insert(lobby_info[3], lobby_info[2])
        db_user_insert(lobby_info[4], lobby_info[2])
        db_set_winner(lobby_info[0], 0)
    elif player_1_points > 21 or player_2_points > 21:
        if player_1_points < player_2_points:
            await bot.send_message(lobby_info[3],
                                   f'Вы выиграли с {player_1_points} против {player_2_points}. +{win_sum} {value}')
            await bot.send_message(lobby_info[4],
                                   f'Вы проиграли с {player_2_points} против {player_1_points}')
            db_user_insert(lobby_info[3], win_sum)
            db_set_winner(lobby_info[0], lobby_info[3])
        else:
            await bot.send_message(lobby_info[4],
                                   f'Вы выиграли с {player_2_points} против {player_1_points}. +{win_sum} {value}')
            await bot.send_message(
                lobby_info[3], f'Вы проиграли с {player_1_points} против {player_2_points}')
            db_user_insert(lobby_info[4], win_sum)
            db_set_winner(lobby_info[0], lobby_info[4])
    else:
        if player_1_points > player_2_points:
            await bot.send_message(lobby_info[3],
                                   f'Вы выиграли с {player_1_points} против {player_2_points}. +{win_sum} {value}')
            await bot.send_message(lobby_info[4],
                                   f'Вы проиграли с {player_2_points} против {player_1_points}')
            db_user_insert(lobby_info[3], win_sum)
            db_set_winner(lobby_info[0], lobby_info[3])
        else:
            await bot.send_message(lobby_info[4],
                                   f'Вы выиграли с {player_2_points} против {player_1_points}. +{win_sum} {value}')
            await bot.send_message(
                lobby_info[3], f'Вы проиграли с {player_1_points} против {player_2_points}')
            db_user_insert(lobby_info[4], win_sum)
            db_set_winner(lobby_info[0], lobby_info[4])


@dp.callback_query_handler(text_startswith='TTT_')
async def ttt_game(call: CallbackQuery):
    call_info = call.data.removeprefix('TTT_').split('_')
    if call_info[1] == 'nothing':
        return
    call_info = list(map(int, call_info))
    lobby_info = db_get_lobby_info(call_info[0])
    other_player = (call_info[1] + 1) % 2
    other_msg = int(str(lobby_info[9]).replace(str(call.message.message_id), ''))
    if lobby_info[8] == 'done' or lobby_info[5] != call_info[1]:
        return
    cur_move = call_info[2] * 3 + call_info[3]
    if lobby_info[8] == 'progress':
        db_set_lobby_status(lobby_info[0], f'{cur_move}:')
    else:
        x_moves, o_moves = lobby_info[8].split(':')
        if lobby_info[7] == call_info[1]:
            x_moves += str(cur_move)
        else:
            o_moves += str(cur_move)
        db_set_lobby_status(lobby_info[0], f'{x_moves}:{o_moves}')
    symbol = '❌' if lobby_info[7] == call_info[1] else '⭕️'
    other_symbol = '⭕️' if symbol == '❌' else '❌'
    await bot.edit_message_text(f'🔴 Ход противника!\n\nВаш знак {symbol}', call.message.chat.id,
                                call.message.message_id,
                                reply_markup=await ttt_table(call_info[0], call_info[1], symbol=symbol,
                                                             x=call_info[2], y=call_info[3],
                                                             prev_key=call.message.reply_markup.inline_keyboard))
    await bot.edit_message_text(f'🟢 Ваш ход!\n\nВаш знак {other_symbol}', lobby_info[3 + other_player],
                                other_msg,
                                reply_markup=await ttt_table(call_info[0], other_player, symbol=symbol,
                                                             x=call_info[2], y=call_info[3],
                                                             prev_key=call.message.reply_markup.inline_keyboard))
    db_set_player_choice(lobby_info[0], 1, other_player)
    if await check_ttt_win(lobby_info[0]):
        return


async def check_ttt_win(lobby_id):
    lobby_info = db_get_lobby_info(lobby_id)
    x_moves, o_moves = lobby_info[8].split(':')
    if len(x_moves) < 3:
        return
    for moves in ttt_win:
        for move in moves:
            if move not in x_moves:
                break
            if move == moves[-1]:
                fee = db_get_fee()
                db_set_lobby_status(lobby_id, 'done')
                win_sum = lobby_info[2] * 2 - ((lobby_info[2] * 2) * (fee / 100))
                await bot.send_message(lobby_info[3 + lobby_info[7]],
                                       f'Вы победили! +{win_sum} {value}')
                await bot.send_message(
                    lobby_info[4 - lobby_info[7]], f'Вы проиграли!')
                db_user_insert(lobby_info[3 + lobby_info[7]], win_sum)
                db_set_winner(lobby_info[0], lobby_info[3 + lobby_info[7]])
                return lobby_info[3 + lobby_info[7]]
    for moves in ttt_win:
        for move in moves:
            if move not in o_moves:
                break
            if move == moves[-1]:
                fee = db_get_fee()
                db_set_lobby_status(lobby_id, 'done')
                win_sum = lobby_info[2] * 2 - ((lobby_info[2] * 2) * (fee / 100))
                await bot.send_message(lobby_info[4 - lobby_info[7]],
                                       f'Вы победили! +{win_sum} {value}')
                await bot.send_message(
                    lobby_info[3 + lobby_info[7]], f'Вы проиграли!')
                db_user_insert(lobby_info[4 - lobby_info[7]], win_sum)
                db_set_winner(lobby_info[0], lobby_info[4 - lobby_info[7]])
                return lobby_info[4 - lobby_info[7]]
