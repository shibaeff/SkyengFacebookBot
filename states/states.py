# Onboarding states
from state import State
#TODO Finish the state
initialState = State(outgoing="""1. Привет 👋. Рассказать вам немного о Skyeng?""" ,
                     user_variants=[],
                     next_states={"Нет": sadOkay})

#TODO Finish the state
sadOkay = State(outgoing="Передумали?",
                user_variants=[],
                next_states={"Передумал": initialState})
