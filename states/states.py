# Onboarding states
from state import State
from keyboard import *
#TODO Finish the state


class InitialState(State):
    def on(self, response):
        if response == "Hi":
            return FirstQustion()

class FirstQuestion(State):
    def on(self, response):
        if response == 'Да' or response == 'Не знаю':
            return ParticularQuestion()
        elif response == 'Нет':
            return SadOkay()

class ParticularQuestion(State):
    def on(self, response):
        if response == 'Skyeng в цифрах':
            return MegaInfo()
        elif response == 'Отзывы студентов':
            return StudentResp()
        elif response == 'Что у вас есть, кроме занятий английским?]':
            return Ausserdem()
        elif response == 'Как это работает?':
            return How()

class MegaInfo(State):
    def on(self, response):
        return Continue()

class StudentResp(State):
    def on(self, response):
        return Continue()

class Ausserdem(State):
    def on(self, response):
        return Continue()

class How(State):
    def on(self, response):
        return Continue()

class Mock(State):
    def on(self, response):
        pass