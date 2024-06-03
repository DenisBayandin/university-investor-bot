import telebot
import os
import numpy as np

from models import *
from config import bot_token
from tinkoff_data import get_prediction

BOT = telebot.TeleBot(bot_token)
COUNT_PREDICTIONS = 0
TICKET_NAME = ""


@BOT.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == "/start":
        BOT.send_message(message.from_user.id, "Напиши аббревиатуру тикета")
        BOT.register_next_step_handler(message, get_ticket_name)
    else:
        BOT.send_message(message.from_user.id, "Введи что-нибудь другое! Для начала введите '/start'")


def get_ticket_name(message):
    global TICKET_NAME
    all_tikets_abbreviation = ", ".join([file.split("_")[0] for file in os.listdir("models")])
    if message.text in all_tikets_abbreviation:
        TICKET_NAME = message.text
        BOT.send_message(message.from_user.id, "На какое количество дней ты хочешь получить прогноз?")
        BOT.register_next_step_handler(message, get_count_predictons)
    else:
        BOT.send_message(message.from_user.id, f"Пока мы не можем дать прогноз на тикет с аббревиатурой {message.text}, выбери "
                                               f"что-то из этого: {all_tikets_abbreviation}")
        BOT.register_next_step_handler(message, get_text_message)


def get_count_predictons(message):
    global COUNT_PREDICTIONS, TICKET_NAME
    COUNT_PREDICTIONS = int(message.text)
    BOT.send_message(message.from_user.id, "Ожидайте... \u2764\u2764\u2764\u2764\u2764")
    BOT.send_photo(message.from_user.id, "https://gas-kvas.com/grafic/uploads/posts/2023-09/1695826322_gas-kvas-com-p-kartinki-s-kotikami-27.jpg")
    result = get_prediction(TICKET_NAME, COUNT_PREDICTIONS)
    BOT.send_message(message.from_user.id,
                     f"Прогноз: {round(result, 2)}" if isinstance(result, float) or
                                                       isinstance(result, int) or
                                                       isinstance(result, np.float32) else
                     "\n".join([f"{index + 1} день: {value_result:.2f} $" for index,
                     value_result in enumerate(result)]))


BOT.polling(none_stop=True, interval=0)
