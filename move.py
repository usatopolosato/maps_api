import pprint

import requests


def move(geocode):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": geocode,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    fi = float(toponym["boundedBy"]['Envelope']['upperCorner'].split()[0]) - float(toponym["boundedBy"]['Envelope']['lowerCorner'].split()[0])
    se = float(toponym["boundedBy"]['Envelope']['upperCorner'].split()[1]) - float(
        toponym["boundedBy"]['Envelope']['lowerCorner'].split()[1])
    return fi, se
