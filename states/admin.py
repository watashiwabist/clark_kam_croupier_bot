from aiogram.dispatcher.filters.state import State, StatesGroup


class settAdmin(StatesGroup):
    addCoupon = State()
    delItem = State()


class spam(StatesGroup):
    post = State()

class qiwi(StatesGroup):
    set_qiwi = State()

class qiwi2(StatesGroup):
    set_qiwi = State()

class yoomoney(StatesGroup):
    set_api = State()

class freekassa(StatesGroup):
    set_api = State()

class fee(StatesGroup):
    fee = State()
