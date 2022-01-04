from aiogram.types import ReplyKeyboardMarkup

from config import button_profile, button_help, button_chat, button_point_game, button_coin_game, \
    button_rock_paper_scissors_game, button_roulette_game, button_tic_tac_toe_game, button_dice_game
# from database import db_select_admins
from database import db_select_admins


async def main_start(user):
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    menu.add(button_coin_game, button_roulette_game)
    menu.add(button_point_game, button_dice_game)
    menu.add(button_rock_paper_scissors_game)
    menu.add(button_tic_tac_toe_game)
    menu.add(button_profile)
    menu.add(button_chat, button_help)
    get_admin = db_select_admins(user)
    if get_admin:
        if get_admin[1] == 2:
            menu.add('Сделать рассылку', 'Купоны')
            menu.add('Сменить API', 'Комиссия')
            menu.add('Состояние')
    return menu
