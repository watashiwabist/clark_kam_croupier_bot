from aiogram.dispatcher.filters.state import State, StatesGroup


class settAdmin(StatesGroup):
    addCatalog = State()
    addSubCatalog = State()
    addProductName = State()
    addProductDescription = State()
    addProductPrice = State()
    addProductImg = State()
    addProductAdminPrice = State()
    addProductData = State()
    addCoupon = State()
    delItem = State()


class spam(StatesGroup):
    post = State()


class transaction(StatesGroup):
    ltc_address = State()
    amount = State()


class changeCoinbase(StatesGroup):
    token = State()
