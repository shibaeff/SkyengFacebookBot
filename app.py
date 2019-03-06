from flask import Flask, request
from logging.handlers import RotatingFileHandler
import logging
import requests
from fbmessenger.bot import Bot


app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'EuDCvM8/KrU2XKAVkvb5TY8TWJOKJRwFf5FsDAU+O54='# <paste your verify token here>
PAGE_ACCESS_TOKEN = 'EAAIyscwep5sBAE6cJF4q8ZAiO0mtUwALzlUiG9GYHKCV0JA9Q1ZClEErXX5m7uQ0hZCRZCvbMoamdcaL4Nz0aoR7AhlEADUvDmPt2XM2Nv7aXP6hasyZBACVbXiDALQD23P5TYLcFx48i6J0S3dKH1NXVLIHGALRLGIiqndgSqgZDZD'# paste your page access token here>"
bot = Bot(validation_token=VERIFY_TOKEN, page_access_token=PAGE_ACCESS_TOKEN)


def send_message(recipient_id, text):
    """
    :param recipient_id: whom to send
    :param text: text to send
    :return: nothing
    """
    payload = {
        'message': {
            # 'text': text
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Try the postback button!",
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Postback Button",
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

    # payload = {
    #   "type": "postback",
    #   "title": "OK",
    #   "payload": "ok"
    # }
    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()


def get_bot_response(message):
    return "Mock '{}'".format(message)


def verify_webhook(req):
    """
    Helper function to verify the successful integration
    with the Facebook API
    :param req: verification request
    :return: verification response
    """
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"


def respond(sender, message):
    """
    Form a response and pipe it to sender
    :param sender:
    :param message:
    :return: nothing
    """
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    """
    Checks if message is from particular user
    :param message: message to check
    :return: is this message from user?
    """
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook", methods=['GET','POST'])
def listen():
    """A webhook for Facebook API calls"""
    app.logger.info("Meth triggered")
    if request.method == 'GET':
        return verify_webhook(request)

    try:
        if request.method == 'POST':
            app.logger.info("Got message with request")
            payload = request.json
            event = payload['entry'][0]['messaging']
            for x in event:
                if is_user_message(x):
                    text = x['message']['text']
                    sender_id = x['sender']['id']
                    respond(sender_id, text)

            return "ok"
    except Exception as e:
        raise e


if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
