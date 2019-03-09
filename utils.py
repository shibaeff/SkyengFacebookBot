from wit import Wit

access_token = "LRH3MMQ4KTUO3BLZJTPWY2BZCOAZTPYW"

client = Wit(access_token = access_token)


def wit_response(message_text):
    POSTIVE = ["12+", "Подтверждаю", "Подтверждаю присутствие родителя", 'something']
    NEGATIVE = ["До 11 лет", "Не подтверждаю", "Ну, что ж, жаль", 'До 18']
    if message_text in POSTIVE:
        return "", 'positive'
    elif message_text in NEGATIVE:
        return '', 'negative'

    resp=client.message(message_text)
    entity = None
    value = None
    try :
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
    except:
        pass
    return(entity,value)



