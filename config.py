# - *- coding: utf- 8 - *-


# Введите токен бота
token_bot = '1633460302:AAEJmLyQy49T46PxiM0IWACJgOdWNAw0LbM'


# ПРИ ИЗМЕНЕНИЕ ТЕКСТА НЕ УДАЛЯТЬ КОВЫЧКИ!
# ПРИ ИЗМЕНЕНИИ ТЕКСТА ЧТОБЫ НАЧАТЬ С НОВОЙ СТРОКИ ТЕКСТ НУЖНО ДОБАВИТЬ '\n' - БЕЗ КОВЫЧЕК
# ПРИМЕР:
#   start_text = 'Hello\nWorld!'
# ВЫВОД:
#   Hello
#   World!
# ЧТОБЫ ИЗМЕНИТЬ СТИЛЬ НАПИСАНИЯ ТЕКСТА ИСПОЛЬЗУЕМ ТАКИЕ СИМВОЛЫ КАК: `, *
# `Hello World` - на разных устройствах разное отображение, обычно используется для
# быстрого копирование выделнной этими символоами строки
# *Hello World* - жирный шрифт

# Введите ID Админа @getmyid_bot
admins = [1518508614]

# Текст после /start
# В последующих обновлениях, это все можно будет изменять через админ. панель
reg_text = 'Регистрация прошла успешно'
auth_text = 'Главное меню'

# Текст для админов
start_text_adm = 'Приветственный текст для админов'

# Текст чата
chat_text = 'Наш чат'
chat_link = 'https://t.me/telegram'

# Текст помощи
help_text = 'По всем вопросам и выплатам - @telegram'

# Обложка магазина
# - написать абсолютный путь до изображения
cover_img = 'image/bnlde25.jpeg'
# Если хотите установить одну единственную обложку для товара, сохраните обложку в корень папки и измените
# переменную на вашу
def_img = 'image/defolt.jpg'
#Картинки к играм
coin_pic = 'image/coin_pic.jpg'
dice_pic = 'image/dice_pic.jpg'
point_pic = 'image/point_pic.jpg'
roulette_pic = 'image/roulette_pic.jpg'
rock_paper_scissors_pic = 'image/RPS_pic.jpg'
tic_tac_toe_pic = 'image/TTT_pic.jpg'

game_pics = {
    '🎮 Монетка': 'image/coin_pic.jpg',
    '🎰 Рулетка': 'image/roulette_pic.jpg',
    '♦️ Очко': 'image/point_pic.jpg',
    '🎲 Кубик': 'image/dice_pic.jpg',
    '✂️ Камень, ножницы, бумага': 'image/RPS_pic.jpg',
    '❌ Крестики-Нолики ⭕️': 'image/TTT_pic.jpg',
}

# Меню
button_profile = '👤 Мой профиль'
button_catalog = '🕹 Каталог'
button_help = '🆘 Помощь'
button_coin_game = '🎮 Монетка'
button_roulette_game = '🎰 Рулетка'
button_point_game = '♦️ Очко'
button_dice_game = '🎲 Кубик'
button_rock_paper_scissors_game = '✂️ Камень, ножницы, бумага'
button_tic_tac_toe_game = '❌ Крестики-Нолики ⭕️'
button_chat = '❗️ Наш чат'



button_changer = 'Убрать это'

# Текст, если товар в каталоге пуст
product_empty_text = 'Убрать это'


catalog_info = 'Убрать это'
product_info = 'Убрать это'

value = '₽'

db = 'db.sqlite'
