# Onboarding states
from state import State
initialState = State(outgoing="""1. Привет 👋. Рассказать вам немного о Skyeng?""" ,
                     buttons=[],
                     next_states={"Нет": sadOkay})

sadOkay = State(outgoing="Передумали?",
                buttons=[],
                next_states={"Передумал": initialState})
