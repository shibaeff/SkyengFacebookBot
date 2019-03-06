class State(object):
    """
    A base class for the Bot's flow
    """
    def __init__(self, outgoing, user_variants, next_states):
        """
        Constructs the state
        :param outgoing: message for the user
        :param user_variants: keyboard/option bar settings
        :param next_states: dictionary directing to the next states
        """
        self.outgoing = outgoing
        self.user_variants = user_variants
        self.next_states = next_states


