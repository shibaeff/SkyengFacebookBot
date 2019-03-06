

class Button(object):
    def __init__(self, recipient_id, text, title):
        self.payload = {
            'message': {
                # 'text': text
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": [
                            {
                                "type": "postback",
                                "title": title,
                                "payload": "DEVELOPER_DEFINED_PAYLOAD"
                            }
                        ]
                    }
                }
            },
            'recipient': {
                'id': recipient_id
            },
            'notification_type': 'regular'
        }


