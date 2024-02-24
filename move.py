import pprint

import requests


def scale_m(geocode):
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


def search_coord(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    return toponym["Point"]["pos"], toponym['metaDataProperty']['GeocoderMetaData']['text']


def postal_index(town):
    try:
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-" \
                           f"98ba-98533de7710b&" \
                           f"geocode={town}&format=json"

        response = requests.get(geocoder_request)
        json_response = response.json()
        tp = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                          'metaDataProperty'][
                          'GeocoderMetaData']['Address']['postal_code']
        return tp
    except Exception as error:
        return 'должно быть произошла какая-то ошибка.'


def get_address(lat, lon):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-" \
                       f"98ba-98533de7710b&" \
                       f"geocode={lon},{lat}&format=json"
    response = requests.get(geocoder_request)
    json_response = response.json()
    tp = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
        'metaDataProperty'][
        'GeocoderMetaData']['Address']['formatted']
    return tp
