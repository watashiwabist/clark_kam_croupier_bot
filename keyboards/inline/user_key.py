from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import chat_link, value
from database import db_get_active_lobby, db_get_user_name
from misc import count_players


async def deposit():
    deposit = InlineKeyboardMarkup()
    deposit.add(
        InlineKeyboardButton('Пополнить баланс', callback_data='USER_PROFILE')
    )
    return deposit


async def profile():
    profile_menu = InlineKeyboardMarkup(row_width=2)
    profile_menu.add(
        InlineKeyboardButton('Пополнить | QIWI', callback_data='TOPUP_qiwi'),
    )
    profile_menu.add(
        InlineKeyboardButton('Пополнить | VISA/MASTERCARD', callback_data='TOPUP_freekassa')
    )
    profile_menu.add(
        InlineKeyboardButton('Заказать вывод', callback_data='WITHDRAW')
    )
    profile_menu.add(
        InlineKeyboardButton('Активировать купон', callback_data='COUPON')
    )
    return profile_menu


async def freekassa_payment_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton('Карта', callback_data='WITHDRAW_freekassa_CARD'),
        InlineKeyboardButton('FKWallet', callback_data='WITHDRAW_freekassa_FKWallet RUB'),
        # InlineKeyboardButton('PERFECT', callback_data='WITHDRAW_freekassa_PERFECT'),
    )
    return markup


async def withdraw_markup():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton('QIWI', callback_data='WITHDRAW_qiwi'),
        InlineKeyboardButton('Freekassa', callback_data='PAYMENT_FREEKASSA')
    )
    return markup


async def game_keyboard(game_name, chat_id):
    active_lobby = db_get_active_lobby(game_name, 'active')
    game_markup = InlineKeyboardMarkup(row_width=2)
    for lobby in active_lobby:
        add = ''
        if game_name == 'roulette_game':
            player_count = count_players(lobby)
            add = f' | {player_count}/5'
        user_name = db_get_user_name(lobby[3])
        who_user_id = ' (Вы) ' if chat_id == lobby[3] else ''
        game_markup.add(
            InlineKeyboardButton(f'🔷 {user_name} {who_user_id}| ставка {lobby[2]} {value}{add}',
                                 callback_data=f'LOBBY_{lobby[0]}-{game_name}-{lobby[2]}-{lobby[3]}')
        )
    game_markup.add(
        InlineKeyboardButton('🗂 Мои игры', callback_data=f'MY_GAMES_{game_name}'),
        InlineKeyboardButton('♻️Обновить', callback_data=f'REFRESH_{game_name}'),
        InlineKeyboardButton('✔️Создать игру', callback_data=f'CREATE_GAME_{game_name}'),
        InlineKeyboardButton('🖥 Статистика', callback_data=f'STATISTICS_{game_name}'),
    )
    return game_markup


async def chat_redirect():
    chat_markup = InlineKeyboardMarkup()
    chat_markup.add(
        InlineKeyboardButton('Перейти в чат', url=chat_link)
    )
    return chat_markup


async def lobby_info(game_id, game_name):
    lobby_info_markup = InlineKeyboardMarkup()
    lobby_info_markup.add(
        InlineKeyboardButton('Играть', callback_data=f'PLAY_{game_id}'),
        InlineKeyboardButton('Отмена', callback_data=f'NOPLAY_{game_name}')
    )
    return lobby_info_markup


async def lobby_owner(game_id):
    lobby_owner_markup = InlineKeyboardMarkup()
    lobby_owner_markup.add(
        InlineKeyboardButton('Удалить', callback_data=f'DELETE_{game_id}')
    )
    return lobby_owner_markup


async def RPS_game(lobby_id, player):
    RPS_game_markup = InlineKeyboardMarkup(row_width=3)
    RPS_game_markup.add(
        InlineKeyboardButton('Камень 🪨', callback_data=f'RPS_ROCK_{lobby_id}_{player}'),
        InlineKeyboardButton('Ножницы ✂️', callback_data=f'RPS_SCISSORS_{lobby_id}_{player}'),
        InlineKeyboardButton('Бумага 📄', callback_data=f'RPS_PAPER_{lobby_id}_{player}'),
    )
    return RPS_game_markup


async def coin_game_markup(lobby_id, player):
    coin_game_markup = InlineKeyboardMarkup()
    coin_game_markup.add(
        InlineKeyboardButton('Орел', callback_data=f'COIN_CHOOSE_eagle_{lobby_id}_{player}'),
        InlineKeyboardButton('Решка', callback_data=f'COIN_CHOOSE_noteagle_{lobby_id}_{player}')
    )
    return coin_game_markup


async def spin_the_roulette(lobby_id):
    spin_the_roulette_markup = InlineKeyboardMarkup()
    spin_the_roulette_markup.add(
        InlineKeyboardButton('Крутить рулетку', callback_data=f'SPIN_{lobby_id}')
    )
    return spin_the_roulette_markup


async def point_choice(lobby_id, player):
    point_choice_markup = InlineKeyboardMarkup()
    point_choice_markup.add(
        InlineKeyboardButton('Взять', callback_data=f'TAKE_{lobby_id}_{player}'),
        InlineKeyboardButton('Хватит', callback_data=f'YETER_{lobby_id}_{player}')
    )
    return point_choice_markup


async def ttt_table(lobby_id, player, symbol=None, x=None, y=None, prev_key=None):
    ttt_table_markup = InlineKeyboardMarkup(row_width=3)
    for i in range(3):
        for j in range(3):
            if x is not None and x == i and y == j:
                ttt_table_markup.insert(InlineKeyboardButton(symbol, callback_data=f'TTT_{lobby_id}_nothing_{i}_{j}'))
            elif symbol is None:
                ttt_table_markup.insert(InlineKeyboardButton('⬜️', callback_data=f'TTT_{lobby_id}_{player}_{i}_{j}'))
            else:
                cd = prev_key[i][j].callback_data
                if cd == 'nothing':
                    ttt_table_markup.insert(InlineKeyboardButton(prev_key[i][j].text, callback_data=cd))
                else:
                    ttt_table_markup.insert(
                        InlineKeyboardButton(prev_key[i][j].text, callback_data=f'TTT_{lobby_id}_{player}_{i}_{j}'))
    return ttt_table_markup


async def payment_info(merchant, pay_url, bill_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton('Оплатить', url=pay_url),
        InlineKeyboardButton('Проверить оплату',
                             callback_data=f'STATUS_PAY_{merchant}_{bill_id}')
    )
    return markup
