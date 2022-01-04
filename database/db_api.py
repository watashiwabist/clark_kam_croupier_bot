# -*- coding: UTF-8 -*-
import datetime
import sqlite3

from config import admins, db


def load_database():
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        # Admin table
        try:
            cur.execute('SELECT * FROM admins')
            print('✅ Connection successful 1/7')
        except sqlite3.DatabaseError:
            print(f'Create admins table 1/7\nAdded an administrator with an ID - {admins}')
            cur.execute('CREATE TABLE IF NOT EXISTS admins('
                        'user_id INT,'
                        'level INT)')
            for a in range(len(admins)):
                cur.execute('INSERT INTO admins VALUES(?, ?)', [admins[a], 2])
        # User table
        try:
            cur.execute('SELECT * FROM users')
            print("✅ Connection successful 2/7")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS users('
                        'user_id INT NOT NULL UNIQUE,'
                        'name TEXT,'
                        'datetime TEXT,'
                        'balance FLOAT,'
                        'ref_id INT,'
                        'UNIQUE ("user_id") ON CONFLICT IGNORE)')
            print("Create users table 2/7")
        # Купон
        try:
            cur.execute('SELECT * FROM coupon')
            print("✅ Connection successful 3/7\n")
        except sqlite3.DatabaseError:
            cur.execute('CREATE TABLE IF NOT EXISTS coupon('
                        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'coup TEXT,'
                        'price INT)')
            print("Create coupon table 3/7\n")
        try:
            cur.execute('SELECT * FROM game_stats')
            print('✅ Connection successful 4/7\n')
        except sqlite3.DatabaseError:
            print('Create game_stats 4/7')
            cur.execute('CREATE TABLE IF NOT EXISTS game_stats('
                        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                        'game TEXT,'
                        'bet_sum INTEGER,'
                        'player_1 INTEGER,'
                        'player_2 INTEGER,'
                        'player_3 INTEGER,'
                        'player_4 INTEGER,'
                        'player_5 INTEGER,'
                        'active TEXT,'
                        'winner INTEGER)')
        try:
            cur.execute('SELECT * FROM config')
            print("✅ Connection successful 5/7\n")
        except sqlite3.DatabaseError:
            print("Create config table 5/7\n")
            cur.execute('CREATE TABLE IF NOT EXISTS config('
                        'id INTEGER,'
                        'fee INTEGER,'
                        'status INTEGER)')
            cur.execute('INSERT INTO config VALUES(0, 0, 1)')
        try:
            cur.execute('SELECT * FROM top_up')
            print("✅ Connection successful 6/7\n")
        except sqlite3.DatabaseError:
            print("Create top_up table 6/7\n")
            cur.execute('CREATE TABLE IF NOT EXISTS top_up('
                        'bill_id TEXT,'
                        'comment TEXT,'
                        'user_id INTEGER,'
                        'amount INTEGER,'
                        'status TEXT,'
                        'date TEXT)')
        try:
            cur.execute('SELECT * FROM merchant')
            print("✅ Connection successful 7/7\n")
        except sqlite3.DatabaseError:
            print("Create merchant table 7/7\n")
            cur.execute('CREATE TABLE IF NOT EXISTS merchant('
                        'id INTEGER,'
                        'qiwi_token TEXT,'
                        'qiwi2_token TEXT,'
                        'yoomoney_token TEXT,'
                        'freekassa_token TEXT)')
            cur.execute('INSERT into merchant VALUES(0, 0, 0, 0, 0)')
    if con:
        con.close()


# Получение юзера по ID
def db_user_info(user):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        # noinspection PyBroadException
        try:
            row = cur.execute('SELECT * FROM users WHERE user_id =?', [user]).fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_user_info: {e}')


def db_select_all_user():
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        # noinspection PyBroadException
        try:
            row = cur.execute('SELECT * FROM users').fetchall()
            return row
        except:
            pass


def db_user_reg(msg):
    cur_msg = msg.text.split()
    ref_id = cur_msg[1] if (len(cur_msg) > 1 and int(cur_msg[1]) != int(msg.from_user.id)) else 0
    print(ref_id)
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            user = [msg.from_user.id, msg.from_user.first_name, datetime.datetime.now().strftime('%Y-%m-%d'), 0, ref_id]
            cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?);', user)
            con.commit()
        except Exception as e:
            print(f'db_api.db_user_reg: {e}')


# Пополнение баланса
def db_user_insert(user=None, amount=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('UPDATE users SET balance=balance+? WHERE user_id=?', [amount, user])
            con.commit()
        except Exception as e:
            print(f'db_api_db_user_insert: {e}')


# Запись о попоплнение баланса
def top_up_insert(user_id, amount, date):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO top_up VALUES(?, ?, ?)', [user_id, amount, date])
        except Exception as e:
            print(f'db_api.top_up_insert: {e}')


def top_up_select(user_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            return cur.execute('SELECT * FROM top_up WHERE user_id=?', [user_id]).fetchall()
        except Exception as e:
            print(f'db_api.top_up_selectt: {e}')


# Измениене баланса
def db_user_update(amount, user):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('UPDATE users SET balance=balance-? WHERE user_id=?', [amount, user])
            con.commit()
        except Exception as e:
            print(f'db_api.db_user_update: {e}')


# Список администраторов
def db_select_admins(user=None):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            if user is None:
                row = cur.execute('SELECT * FROM admins').fetchall()
                return row
            else:
                row = cur.execute('SELECT * FROM admins WHERE user_id=?', (user,)).fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_select_admins: {e}')


def db_select_id_admins():
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM admins WHERE level=?', [2]).fetchall()
            return row
        except Exception as e:
            print(f'db_api.db_select_id_admins: {e}')


# Добавление администратора
def db_insert_admin(user_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO admins(user_id, level) VALUES (?, ?)', [user_id, 1])
        except Exception as e:
            print(f'db_insert_admin: {e}')


# Удаление администратор
def db_delete_admin(user_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM admins WHERE user_id=?', [user_id])
        except Exception as e:
            print(f'db_api.db_delete_admin: {e}')


def db_insert_coupon(coup, price):
    with sqlite3.connect('db.sqlite') as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO coupon(coup, price) VALUES(?, ?)', [coup, price])
        except Exception as e:
            print(f'db_api.db_insert_coupon: {e}')


def db_select_coupon(text=None):
    with sqlite3.connect('db.sqlite') as con:
        cur = con.cursor()
        try:
            if text is None:
                row = cur.execute('SELECT * FROM coupon').fetchall()
            else:
                row = cur.execute('SELECT * FROM coupon WHERE coup=?', [text]).fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_select_coupon: {e}')


def db_delete_coupon(id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM coupon WHERE id=?', [id])
        except Exception as e:
            print(f'db_api.db_delete_coupon: {e}')


def db_get_user_balance(id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT balance FROM users WHERE user_id=?', [id]).fetchone()
            return row[0]
        except Exception as e:
            print(f'd_api.db_get_user_balance: {e}')


def db_create_game_lobby(id, bet_sum, game):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO game_stats(game, bet_sum, player_1, active) VALUES(?, ?, ?, ?)',
                        [game, bet_sum, id, 'active'])
            lid = cur.lastrowid
            return lid
        except Exception as e:
            print(f'd_api.db_create_game_lobby: {e}')


def db_get_refs(user_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM users WHERE ref_id=?', [user_id]).fetchall()
            return len(row)
        except Exception as e:
            print(f'd_api.db_get_refs: {e}')


def db_get_game_history(user_id, game):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        player_num = 3 if game != 'roulette_game' else 6
        try:
            row = []
            for i in range(1, player_num):
                cur_row = cur.execute(f'SELECT * FROM game_stats WHERE game=? AND player_{i}=?',
                                      [game, user_id]).fetchall()
                for item in cur_row:
                    row.append(item)
            return row
        except Exception as e:
            print(f'd_api.db_get_game_history: {e}')


def db_get_active_lobby(game, status):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM game_stats WHERE game=? AND active=?', [game, status]).fetchall()
            return row
        except Exception as e:
            print(f'd_api.db_get_active_lobby: {e}')


def db_get_user_name(user_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT name FROM users WHERE user_id=?', [user_id]).fetchone()
            return row[0]
        except Exception as e:
            print(f'd_api.db_get_user_name: {e}')


def db_delete_lobby(lobby_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM game_stats WHERE id=?', [lobby_id])
        except Exception as e:
            print(f'db_api.db_delete_lobby: {e}')


def db_get_game_name(lobby_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT game FROM game_stats WHERE id=?', [lobby_id]).fetchone()
            return row[0]
        except Exception as e:
            print(f'db_api.db_get_game_name: {e}')


def db_check_game_available(lobby_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT active FROM game_stats WHERE id=?', [lobby_id]).fetchone()
            return row[0]
        except Exception as e:
            print(f'db_api.check_game_available: {e}')
            return 'deleted'


def db_get_player_id(lobby_id, player):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute(f'SELECT player_{player} FROM game_stats WHERE id=?', [lobby_id]).fetchone()
            return row[0]
        except Exception as e:
            print(f'db_api.db_get_player: {e}')


def db_join_lobby(lobby_id, user_id, player):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute(f'UPDATE game_stats SET player_{player}=? WHERE id=?', [user_id, lobby_id])
            con.commit()
        except Exception as e:
            print(f'db_api.db_join_lobby: {e}')


def db_get_lobby_bet(lobby_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute(f'SELECT bet_sum FROM game_stats WHERE id=?', [lobby_id]).fetchone()
            return row[0]
        except Exception as e:
            print(f'db_api.db_get_lobby_bet: {e}')


def db_set_lobby_status(lobby_id, status):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute(f'UPDATE game_stats SET active=? WHERE id=?', [status, lobby_id])
            con.commit()
        except Exception as e:
            print(f'db_api.db_set_lobby_status: {e}')


def db_set_deck(lobby_id, deck):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute(f'UPDATE game_stats SET active=? WHERE id=?', [deck, lobby_id])
            con.commit()
        except Exception as e:
            print(f'db_api.db_set_deck: {e}')


def db_get_lobby_info(lobby_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute(f'SELECT * FROM game_stats WHERE id=?', [lobby_id]).fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_get_lobby_bet: {e}')


def db_set_player_choice(lobby_id, player, choice):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute(f'UPDATE game_stats SET player_{player + 2}=? WHERE id=?', [choice, lobby_id])
            con.commit()
        except Exception as e:
            print(f'db_api.db_set_player_choice: {e}')


def db_set_winner(lobby_id, winner_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('UPDATE game_stats SET winner=? WHERE id=?', [winner_id, lobby_id])
            # cur.execute('UPDATE game_stats SET active=? WHERE id=?', ['done', lobby_id])
            con.commit()
        except Exception as e:
            print(f'db_api.db_set_winner: {e}')


def db_set_fee(fee):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute(f'UPDATE config SET fee=? WHERE id=?', [fee, 0])
            con.commit()
        except Exception as e:
            print(f'db_api.db_set_fee: {e}')


def db_get_fee():
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute(f'SELECT fee FROM config WHERE id=?', [0]).fetchone()
            return row[0]
        except Exception as e:
            print(f'db_api.db_get_fee: {e}')


def db_set_merchant_token(token, merchant):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute(f'UPDATE merchant SET {merchant}_token=? WHERE id=?', [token, 0])
            con.commit()
        except Exception as e:
            print(f'db_api.db_set_merchant_token: {e}')


def db_get_merchant_token(merchant):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute(f'SELECT {merchant}_token FROM merchant WHERE id=?', [0]).fetchone()
            return row[0]
        except Exception as e:
            print(f'db_api.db_get_merchant_token: {e}')


def db_insert_bill(bill_id, user_id, amount, date, status='progress', comment=None):
    if comment is None:
        comment = 'comment'
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO top_up(bill_id, user_id, amount, comment, date, status) VALUES(?, ?, ?, ?, ?, ?)',
                        [bill_id, user_id, amount, comment, date, status])
            con.commit()
        except Exception as e:
            print(f'd_api.db_insert_bill: {e}')


def db_get_bill(bill_id, user_id):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM top_up WHERE bill_id=? and user_id=?',
                              [bill_id, user_id]).fetchone()
            return row
        except Exception as e:
            print(f'db_api.db_get_bill: {e}')


def db_change_status(bill_id, status='done'):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute(f'UPDATE top_up SET status=? WHERE bill_id=?', [status, bill_id])
            con.commit()
        except Exception as e:
            print(f'db_api.db_change_status: {e}')


def db_check_comments(comment):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM top_up WHERE comment=?',
                              [comment]).fetchall()
            return False if len(row) > 0 \
                else True
        except Exception as e:
            print(f'db_api.db_check_comments: {e}')


def db_get_bot_status():
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT status FROM config WHERE id=?',
                              [0]).fetchone()
            return row[0]
        except Exception as e:
            print(f'db_api.db_check_comments: {e}')


def db_set_bot_status(status):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            cur.execute('UPDATE config SET status=? WHERE id=?',
                        [status, 0])
        except Exception as e:
            print(f'db_api.db_check_comments: {e}')


def db_get_all_games_stat(game):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        try:
            row = cur.execute('SELECT * FROM game_stats WHERE game=?',
                              [game]).fetchall()
            return row
        except Exception as e:
            print(f'db_api.db_get_all_games_stat: {e}')
