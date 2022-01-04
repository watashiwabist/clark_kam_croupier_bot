from aiogram.dispatcher.filters.state import State, StatesGroup


class settUser(StatesGroup):
    topUp = State()
    coupon = State()


class Game(StatesGroup):
    create_lobby = State()


class withdraw(StatesGroup):
    amount = State()
    account = State()
