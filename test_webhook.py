from unittest import TestCase
from unittest import main as umain
from Keyboard import Keyboard
from utils import wit_response




def send_message(sender_id, keyboard):
    print("$$ Sending to %s" % sender_id)
    print("%s ::::\n %s" % (keyboard.get_text(), str([item['title'] for item in keyboard.get_buttons()])))


def save_user_email():
    pass


def get_days():
    return ["20/02", "21/02"]


def check_for_existance():
    return True


def write_day(day):
    pass


def get_time():
    return ["14:00", "17:00"]


def write_time():
    pass

STATES = dict()
ENLISTING = set()


class TestWebhook(TestCase):
    def enlisting(self, sender_id, pipeline, states):
        for messaging_text, assert_state in zip(pipeline, states):
            current_state = STATES[sender_id]
            entity, value = wit_response(messaging_text)

            self.assertEquals(current_state, assert_state)
            if current_state == "wait_time":
                write_time()
                send_message(sender_id,
                             Keyboard(
                                 text="🎉 Вы записаны. ВУ пройдет {{intro_lesson_date}} в {{intro_lesson_time}}. До встречи!"
                                      "Если передумаете, отменить или изменить запись можно в личном кабинете.",
                                 titles=None
                             ))
                send_message(sender_id,
                             Keyboard(
                                 text="Добавить в календарь?",
                                 titles=["Да", "Нет"]
                             ))
                STATES[sender_id] = 'calendar_wait'

            elif current_state == "wait_days":
                write_day(messaging_text)
                send_message(sender_id,
                             Keyboard(
                                 text="👍Great! А теперь выберите удобное время",
                                 titles=get_time()
                             ))
                STATES[sender_id] = "wait_time"

            elif current_state == 'enlisting_start':
                send_message(sender_id, Keyboard(
                    text="Привет 👋 Я запишу вас на бесплатный урок в онлайн-школу английского языка Skyeng."
                         "Давайте проверим, есть ли у вас аккаунт. Он нужен для регистрации на занятие и для доступа на платформу, где будет проходить урок. Если аккаунта нет — я его создам."
                         "Пожалуйста, введите ваш email.",
                    titles=None
                ))
                STATES[sender_id] = 'wait_email'
            elif current_state == 'wait_email':
                save_user_email()
                send_message(sender_id,
                             Keyboard(
                                 text="Отлично! Теперь укажите возраст ученика",
                                 titles=["До 18", "18+"]
                             ))
                STATES[sender_id] = 'wait_age'
            elif current_state == 'wait_age':
                if value == 'positive':
                    if check_for_existance():
                        send_message(sender_id,
                                     Keyboard(
                                         text="Ура! У вас уже есть аккаунт :)"
                                              "Если вы забыли пароль, можно установить новый по ссылке {{password_reset_link}}"
                                              "Чтобы включить программу чтения с экрана, нажмите Ctrl+Alt+Z. Для просмотра списка быстрых клавиш нажмите Ctrl+косая черта.",
                                         titles=None
                                     ))
                    else:
                        send_message(sender_id,
                                     Keyboard(
                                         text="💫 Done! Я создал вам аккаунт в Skyeng. "
                                              "Логин: {{customer.email}}, пароль от личного кабинета придет вам на почту.",
                                         titles=None
                                     ))
                else:
                    pass
                days = get_days()
                send_message(sender_id, Keyboard(
                    text="Выберите день, на который хотите записаться 🗓️",
                    titles=days
                ))
                STATES[sender_id] = "wait_days"

    def webhook(self, pipeline, states_line):
        # log(data)

        sender_id = 13

        for (messaging_text, assert_state) in zip(pipeline, states_line):
            if sender_id in ENLISTING:
                self.enlisting(sender_id, messaging_text)
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
                elif value == 'positive':

                    STATES[sender_id] = 'enlisting_start'
                    ENLISTING.add(sender_id)
                    self.enlisting(sender_id, messaging_text)
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

    # def test_simple_greeting(self):
    #     pipeline = ["Привет", 'Да', 'Нет']
    #     states_line = ["initial", 'initial_wait', 'continuation_wait']
    #     self.webhook_mock(pipeline, states_line)

    # def test_simple_back_to_greeting(self):
    #     pipeline = ["Привет", 'Нет', 'Передумали?']
    #     states_line = ["initial", 'initial_wait', 'initial_wait']
    #     self.webhook_mock(pipeline, states_line)

    # def test_simple_without_info(self):
    #     pipeline = ["Привет", 'Нет', 'Передумали?']
    #     states_line = ["initial", 'initial_wait', 'initial_wait']
    #     self.webhook(pipeline, states_line)
    # def test_proceed_to_age_selection(self):
    #     pipeline = ["Привет", "Да", "Skyeng в цифрах", "Нет", "Да", "До 18"]
    #     states_line = ["initial", "intial_wait", "info_wait", "continue", "thankyou_wait", "wait_age"]

    def test_enlisting(self):
        ENLISTING.add(13)
        STATES[13] = "enlisting_start"
        self.enlisting(pipeline=[], states=[])
if __name__ == "__main__":
    umain()



