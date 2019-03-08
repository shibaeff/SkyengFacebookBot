from unittest import TestCase
from unittest import main as umain
from Keyboard import Keyboard
from utils import wit_response




def send_message(sender_id, keyboard):
    print("$$ Sending to %s" % sender_id)
    print("%s ::::\n %s" % (keyboard.get_text(), str([item['title'] for item in keyboard.get_buttons()])))


class TestWebhook(TestCase):
    def webhook_mock(self, pipeline, states_line):
        # log(data)
        STATES = dict()
        sender_id = 13
        for messaging_text, assert_state in zip(pipeline, states_line):
            entity, value = wit_response(messaging_text)
            current_state = STATES.get(sender_id, 'initial')
            self.assertEquals(current_state, assert_state)
            if current_state == "info_wait":
                if value == "somethingelse":
                    send_message(sender_id, Keyboard(
                        titles=[],
                        text="Skyeng Magazine — онлайн-журнал о том, как перестать бояться английского, узнать его получше и полюбить. Читать: https://magazine.skyeng.ru/"
                            "YouTube-канал — нескучный английский с Таней Стариковой и американцем Дэниелом. Смотреть: https://www.youtube.com/user/skyengschool"
                            "Бесплатное приложение Skyeng — учите новые слова. Единый словарь для ваших уроков, тематических наборов, фильмов и песен. Установить: {{app_download_link}}"
                            "Расширение для браузера — добавляйте в приложение Skyeng слова с сайтов при помощи расширения для браузера. Установить: {{extension_download_link}}"
                            "'Полезные' письма — бесплатные email-курсы про английский язык. Выбрать: https://school.skyeng.ru/mailing"
                            "Вебинары — бесплатные тематические онлайн-лекции. Афиша: http://webinar.skyeng.ru/afisha"
                    ))
                    STATES[sender] = "continue"
                    send_message(sender_id, Keyboard(titles=["Да", "Нет"],
                                                     text="Продолжим?"))
                elif value == "feedback":
                    send_message(sender_id, Keyboard(
                        text="Skyeng - топ! Отвечаю",
                        titles=[]
                    ))
                    STATES[sender] = "continue"
                    send_message(sender_id, Keyboard(titles=["Да", "Нет"],
                                                     text="Продолжим?"))
                elif value == "numbers":
                    STATES[sender] = "continue"
                    send_message(sender_id, Keyboard(titles=[],
                                                     text="Skyeng — это онлайн-школа английского языка нового поколения. В школе работают профессионалы, помогающие жителям современных мегаполисов выучить английский язык в условиях недостатка времени."
                                                     "\n5460 преподавателей\n58700 учеников\n4218000 уроков проведено с момента основания\n"
                                                      "50 минут — продолжительность урока\n24 часа в сутки — идут занятия в школе\n1-й урок — бесплатно\nпреподавателем Skyeng становится только 1 из 36 кандидатов"))
                    send_message(sender_id, Keyboard(titles=["Да", "Нет"],
                                                     text="Продолжим?"))
                elif value == "how":
                    STATES[sender] = "continue"
                    send_message(sender_id, Keyboard(titles=["Да", "Нет"],
                                                     text="Продолжим?"))
            elif current_state == "continuation_wait":
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
            elif current_state == 'initial_wait':
                if value == 'positive' or value == 'neutral':
                    send_message(Keyboard(
                        text="Что вам было бы интересно узнать?",
                        titles=[
                            "Skyeng в цифрах",
                            "Отзывы студентов",
                            "Что у вас есть, кроме занятий английским?",
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

    # def test_simple_greeting(self):
    #     pipeline = ["Привет", 'Да', 'Нет']
    #     states_line = ["initial", 'initial_wait', 'continuation_wait']
    #     self.webhook_mock(pipeline, states_line)

    # def test_simple_back_to_greeting(self):
    #     pipeline = ["Привет", 'Нет', 'Передумали?']
    #     states_line = ["initial", 'initial_wait', 'initial_wait']
    #     self.webhook_mock(pipeline, states_line)

    def test_simple_without_info(self):
        pipeline = ["Привет", 'Нет', 'Передумали?']
        states_line = ["initial", 'initial_wait', 'initial_wait']
        self.webhook_mock(pipeline, states_line)
if __name__ == "__main__":
    umain()



