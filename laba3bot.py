import telebot
import sqlite3

bot = telebot.TeleBot('6350229764:AAGWlVarulCL_dQEu3t8r3iQkClzqHjqWhc')
name = None


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('basa.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT)')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, это регистрация. Введи имя.')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('basa.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, password) VALUES (?, ?)', (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Все пользователи', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    conn = sqlite3.connect('basa.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()  # Corrected method name
    info = ''
    for user in users:
        info += f'{user[0]} Имя:{user[1]} Пароль: {user[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)  # Use call.message.chat.id for sending the message
bot.polling(none_stop=True)