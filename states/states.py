# Onboarding states
from state import State
initialState = State(outgoing="""1. Привет 👋. Рассказать вам немного о Skyeng?""" ,
                     user_variants=[],
                     next_states={"Нет": sadOkay})

sadOkay = State(outgoing="Передумали?",
                user_variants=[],
                next_states={"Передумал": initialState})
