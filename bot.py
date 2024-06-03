import telebot
import os

from models import *
from config import bot_token
from tinkoff_data import get_prediction

bot = telebot.TeleBot(bot_token)
count_predictions = 0
ticket_name = ""


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Напиши аббревиатуру тикета")
        bot.register_next_step_handler(message, get_ticket_name)
    else:
        bot.send_message(message.from_user.id, "Введи что-нибудь другое! Для начала введите '/start'")


def get_ticket_name(message):
    global ticket_name
    all_tikets_abbreviation = ", ".join([", ".join([file.split("_")[0] for file in os.listdir("models")])])
    if message.text in all_tikets_abbreviation:
        ticket_name = message.text
        bot.send_message(message.from_user.id, "На какое количество дней ты хочешь получить прогноз?")
        bot.register_next_step_handler(message, get_count_predictons)
    else:
        bot.send_message(message.from_user.id, f"Пока мы не можем дать прогноз на тикет с аббревиатурой {message.text}, выбери "
                                               f"что-то из этого: {all_tikets_abbreviation}")
        bot.register_next_step_handler(message, get_text_message)


def get_count_predictons(message):
    global count_predictions, ticket_name
    count_predictions = int(message.text)
    bot.send_message(message.from_user.id, "Ожидайте... \u2764\u2764\u2764\u2764\u2764")
    bot.send_photo(message.from_user.id, "https://gas-kvas.com/grafic/uploads/posts/2023-09/1695826322_gas-kvas-com-p-kartinki-s-kotikami-27.jpg")
    result = get_prediction(ticket_name, count_predictions)
    bot.send_message(message.from_user.id,
                     round(result, 2) if isinstance(result, float) or isinstance(result, int) else
                     "\n".join([f"{index + 1} день: {value_result:.2f} \u20BD" for index,
                     value_result in enumerate(result)]))


bot.polling(none_stop=True, interval=0)
