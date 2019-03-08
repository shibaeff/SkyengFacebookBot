import os, sys
import datetime as dt
from flask import Flask, request, session
from utils import wit_response
import json
import requests
from pymessenger import Bot
from fbmq import Page, Attachment, Template, QuickReply
from flask_sqlalchemy import SQLAlchemy
from numpy import random
from Keyboard import Keyboard

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAIyscwep5sBAE6cJF4q8ZAiO0mtUwALzlUiG9GYHKCV0JA9Q1ZClEErXX5m7uQ0hZCRZCvbMoamdcaL4Nz0aoR7AhlEADUvDmPt2XM2Nv7aXP6hasyZBACVbXiDALQD23P5TYLcFx48i6J0S3dKH1NXVLIHGALRLGIiqndgSqgZDZD'
bot = Bot(PAGE_ACCESS_TOKEN)
page = Page(PAGE_ACCESS_TOKEN)
STATES = dict()

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "A":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

def enlisting():
    pass

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                sender_id = str(messaging_event['sender']['id'])
                recipient_id = str(messaging_event['recipient']['id'])

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text:'

                    # print(sender_id)

                    response = "none"
                    entity, value = wit_response(messaging_text)
                    current_state = STATES.get(sender_id, 'initial')
                    # self.assertEquals(current_state, assert_state)
                    if current_state == "info_wait":
                        if value == "somethingelse":
                            # TODO optimize this button
                            send_message(sender_id, Keyboard(
                                text="Skyeng Magazine — онлайн-журнал о том, как перестать бояться английского, узнать его получше и полюбить. Читать: https://magazine.skyeng.ru/"
                                     "YouTube-канал — нескучный английский с Таней Стариковой и американцем Дэниелом. Смотреть: https://www.youtube.com/user/skyengschool"
                                     "Бесплатное приложение Skyeng — учите новые слова. Единый словарь для ваших уроков, тематических наборов, фильмов и песен. Установить: {{app_download_link}}"
                                     "Расширение для браузера — добавляйте в приложение Skyeng слова с сайтов при помощи расширения для браузера. Установить: {{extension_download_link}}"
                                     "'Полезные' письма — бесплатные email-курсы про английский язык. Выбрать: https://school.skyeng.ru/mailing"
                                     "Вебинары — бесплатные тематические онлайн-лекции. Афиша: http://webinar.skyeng.ru/afisha"
                            ))
                            app.logger.info("something else")
                            STATES[sender] = "continue"
                            send_message(sender_id, Keyboard(titles=["Да", "Нет"],
                                                             text="Продолжим?"))
                        elif value == "feedback":
                            send_message(sender_id, Keyboard(
                                text="Skyeng - топ! Отвечаю",
                                titles=[]
                            ))
                            STATES[sender_id] = "continue"
                            app.logger.info("FEEDBACKS!!")
                            send_message(sender_id, Keyboard(titles=["Да", "Нет"],
                                                             text="Продолжим?"))
                        elif value == "numbers":
                            STATES[sender_id] = "continue"
                            send_message(sender_id, Keyboard(titles=None,
                                                             text="Skyeng — это онлайн-школа английского языка нового поколения. В школе работают профессионалы, помогающие жителям современных мегаполисов выучить английский язык в условиях недостатка времени."
                                                                  "\n5460 преподавателей\n58700 учеников\n4218000 уроков проведено с момента основания\n"
                                                                  "50 минут — продолжительность урока\n24 часа в сутки — идут занятия в школе\n1-й урок — бесплатно\nпреподавателем Skyeng становится только 1 из 36 кандидатов"))
                            send_message(sender_id, Keyboard(titles=["Да", "Нет"],
                                                             text="Продолжим?"))
                        elif value == "how":
                            STATES[sender_id] = "continue"
                            send_message(sender_id,
                                         Keyboard(
                                             titles=None,
                                             text="Как проходят уроки в Skyeng — https://magazine.skyeng.ru/vimbox/\n"
                                                  "Про приложение Skyeng — https://magazine.skyeng.ru/skyeng-app/"

                                         ))
                            send_message(sender_id, Keyboard(titles=["Да", "Нет"],
                                                             text="Продолжим?"))
                    elif current_state == "thank_you_wait":
                        # TODO enlisting routine
                        if value == 'negative':
                            send_message(sender_id,
                                         Keyboard(titles=None,
                                                  text="Пока!!!")
                                         )
                            STATES[sender_id] = 'initial'
                    elif current_state == "continue":
                        if value == 'negative':
                            send_message(sender_id, Keyboard(
                                text="Приятно было пообщаться 🤗\n"
                                     "Хотите записаться на бесплатный урок английского?\n"
                                     "Занятие длится 50 минут и проходит онлайн. На нем:\n"
                                     "✔️Сформулируем ваши цели\n"
                                     "✔️Определим уровень английского\n"
                                     "✔️Расскажем про учебную платформу\n",
                                titles=['Да', "Нет"]
                            ))
                            STATES[sender_id] = "thank_you_wait"
                        elif value == 'positive':
                            send_message(sender_id, Keyboard(
                                text="Что вам было бы интересно узнать?",
                                titles=[
                                    "Skyeng в цифрах",
                                    "Отзывы студентов",
                                    # "Что есть кроме английского?", TODO optimize
                                    "Как это работает?"
                                ]
                            ))
                            STATES[sender_id] = "info_wait"
                    elif current_state == 'initial_wait':
                        if value == 'positive' or value == 'neutral':
                            send_message(sender_id, Keyboard(
                                text="Что вам было бы интересно узнать?",
                                titles=[
                                    "Skyeng в цифрах",
                                    "Отзывы студентов",
                                    # "Что есть кроме английского?", TODO optimize
                                    "Как это работает?"
                                ]
                            ))
                            STATES[sender_id] = "info_wait"
                        if value == 'negative':
                            send_message(sender_id, Keyboard(
                                text="Окей 🤐",
                                titles=["Передумали?"]
                            ))
                        if value == 'once_again':
                            STATES['sender_id'] = 'initial_wait'
                            send_message(sender_id, Keyboard(titles=['Да', 'Нет', 'Не знаю'],
                                                             text='Привет 👋 Рассказать вам немного о Skyeng?'))
                    elif value == "greeting" or current_state == 'initial':
                        send_message(sender_id, Keyboard(titles=['Да', 'Нет', 'Не знаю'],
                                                         text='Привет 👋 Рассказать вам немного о Skyeng?'))
                        STATES[sender_id] = 'initial_wait'

                    return "ok", 200
    return "ok", 200


def send_message(sender_id, keyboard):
    if keyboard.get_buttons() != None and keyboard.get_buttons() != []:
        page.send(sender_id,
                  keyboard.get_text(),
                  quick_replies=keyboard.get_buttons())
    else:
        page.send(sender_id,
                  keyboard.get_text())



if __name__ == "__main__":
    app.secret_key = "secret"
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
