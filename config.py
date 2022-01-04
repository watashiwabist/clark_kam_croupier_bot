# - *- coding: utf- 8 - *-


# Введите токен бота
token_bot = '5080629444:AAGBRR14IG6v23cfihPn6VEniGp8A3_czuc'

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

# Текст чата
chat_text = 'Наш чат'
chat_link = 'https://t.me/telegram'

# Текст помощи
help_text = 'По всем вопросам и выплатам - @Pi3r0777'

# ID магазина free-kassa
shop_id = 8533
merchant_id = 8533
secret_word = 'm[-fV,Kxv?kBw_U'
freekassa_api = 'c2d577edc7e9266d7c6abdb7e672df2e'

# минимальная сумма пополнения
min_top_up = 100

# Обложка магазина
# - написать абсолютный путь до изображения
cover_img = 'image/bnlde25.jpeg'
# Если хотите установить одну единственную обложку для товара, сохраните обложку в корень папки и измените
# переменную на вашу
def_img = 'image/defolt.jpg'
# Картинки к играм
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

deck = [6, 7, 8, 9, 10, 2, 3, 4, 11] * 4

game_pics2 = {
    'coin_game': 'image/coin_pic.jpg',
    'roulette_game': 'image/roulette_pic.jpg',
    'point_game': 'image/point_pic.jpg',
    'dice_game': 'image/dice_pic.jpg',
    'rock_paper_scissors_game': 'image/RPS_pic.jpg',
    'tic_tac_toe_game': 'image/TTT_pic.jpg',
}

gifs = {
    0: 'gif/eagle',
    1: 'gif/not_eagle'
}

ttt_win = ['012', '036', '147', '258', '246', '345', '678', '048']

roulette_caption = 'Игроки:\n\n' \
                   'Добавился новый игрок:\n\n' \
                   '🟥 1 (Свободное место)\n' \
                   '🟪 2 (Свободное место)\n' \
                   '🟦 3 (Свободное место)\n' \
                   '🟩 4 (Свободное место)\n' \
                   '🟧 5 (Свободное место)\n'

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

game_names = {
    'point_game': button_point_game,
    'coin_game': button_coin_game,
    'roulette_game': button_roulette_game,
    'dice_game': button_dice_game,
    'tic_tac_toe_game': button_tic_tac_toe_game,
    'rock_paper_scissors_game': button_rock_paper_scissors_game,
}

rps = {
    'ROCK': 1,
    'SCISSORS': 2,
    'PAPER': 3
}

value = '₽'

db = 'db.sqlite'
