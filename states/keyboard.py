class Button(dict):
    def __init__(self, title):
        self["type"] = "postback"
        self["title"] = title
        self["payload"] = title


class Keyboard(object):
    def __init__(self, text, buttons_list):
        self.payload = {
            'message': {
                'text': text,
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons_list
                    }
                }
            },
            # 'recipient': {
            #     'id': recipient_id
            # },
            'notification_type': 'regular'
        }


