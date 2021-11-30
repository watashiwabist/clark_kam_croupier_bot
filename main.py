# -*- coding: UTF-8 -*-
# from db import start_database
from database import load_database

load_database()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp)
