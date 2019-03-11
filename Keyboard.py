class Keyboard(object):
    def __init__(self, titles=None, text=None):
        self.Text = None
        if text is not None:
            self.Text = text
        self.Buttons = []
        if titles is not None:
            self.Buttons = [{'title': title, 'payload' : 'pick_action'} for title in titles]

    def get_buttons(self):
        return self.Buttons

    def get_text(self):
        return self.Text
