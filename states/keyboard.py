class Button(dict):
    def __init__(self, title):
        self["type"] = "postback"
        self["title"] = title
        self["payload"] = "DEVELOPER_DEFINED_PAYLOAD"


class Keyboard(object):
    def __init__(self, recipient_id, text, buttons_list):
        self.payload = {
            'message': {
                # 'text': text
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons_list
                    }
                }
            },
            'recipient': {
                'id': recipient_id
            },
            'notification_type': 'regular'
        }


