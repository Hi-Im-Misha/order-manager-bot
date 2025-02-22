import telebot
from telebot import types
import pandas as pd
import json
from queueRabbit import send_to_queue

with open(r'Git_project\telegram_bot\create_cart_bot_telegram\bot_forwarder_telegram\config.json', 'r') as f:
    config = json.load(f)
bot_token = config['bot_token']
user_id = config['user_id']
user_id_tuner = config['user_id_tuner']

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Оформить Заказ')
    item2 = types.KeyboardButton('Связь с продавцом')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'привет', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Оформить Заказ')
def buy(message):
    bot.send_message(message.chat.id, 'Введите ID или название товара \nкоторый хотите купить')
    bot.register_next_step_handler(message, order_registration)


@bot.message_handler(func=lambda message: message.text == 'Связь с продавцом')
def contact_seller(message):
    bot.send_message(message.chat.id, '@...') # seller's ID



@bot.message_handler(func=lambda message: True)
def order_registration(message):
    product = message.text
    order_data = {'product': product, 'user_id': user_id}
    send_to_queue(order_data, 'orders_queue')
    try:
        df = pd.read_excel(r'C:\mylife\Git_project\telegram_bot\create_cart_bot_telegram\bot_forwarder_telegram\catalog.xlsx') # file path
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        product = message.text
    
    try:
        if product in df.iloc[:, [0, 1]].values.flatten():
            index = df[(df.iloc[:, 0] == product) | (df.iloc[:, 1] == product)].index[0]
            global value, products, ID
            ID = df.iloc[index, 1]
            products = df.iloc[index, 0]
            value = df.iloc[index, 16]



            keyboard = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Оплатить через Карту', callback_data='button1_clicked')
            button2 = types.InlineKeyboardButton('Оплатить при встрече', callback_data='button2_clicked')
            keyboard.add(button1)
            keyboard.add(button2)
            bot.send_message(message.chat.id, f'Спасибо за заказ. \n{products} - {value} \nЕсли все верно \nМожно оплатить сразу или при получении товара', reply_markup=keyboard)

        else:
            # bot.send_message(user_id, f'Пользователь попытался купить Товара "{product}" нет в наличии')
            bot.send_message(message.chat.id, 'Товара нет в наличии')



    except Exception as e:
        
        print(f"Error reading the Excel file: {e}")
        bot.send_message(user_id_tuner, "Error reading the Excel file")



    
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        if call.message:
            if call.data == 'button1_clicked':
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton('Оплатил', callback_data='paid')
                keyboard.add(button1)
                bot.send_message(call.message.chat.id, f'К оплате {value}\nбанк1 - 123\nбанк2 - 456\nбанк3 - 789', reply_markup=keyboard) # bank card
                
            if call.data == 'paid':
                bot.send_message(call.message.chat.id, 'Спасибо за оплату \nОжидайте ответа.')
                bot.send_message(user_id, f'Пользователь @{call.from_user.username}\nЗаказал товар: {products}\nID товара: {ID}\nОплатил: {value}')



            if call.data == 'button2_clicked':
                bot.send_message(call.message.chat.id, 'Спасибо за заказ \nОжидайте ответа.')
                bot.send_message(user_id, f'Пользователь @{call.from_user.username} \nЗаказал товар: {products}\nОплата при встрече')

    except Exception as e:
        print(f"Callback processing error: {e}")
        bot.send_message(user_id_tuner, "Callback processing error")






bot.polling()

