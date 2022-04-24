import requests

from src.api.api import Api, UseApikey


class Geocoder(UseApikey, Api):
    URL = 'http://geocode-maps.yandex.ru/1.x/'

    @classmethod
    def get_pos(cls, response: requests.Response) -> tuple or None:
        json_response = response.json()
        features = \
            json_response['response']['GeoObjectCollection']['featureMember']

        if len(features) == 0 or not response:
            return

        geocode = json_response['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']
        geocode_pos = tuple(map(float, geocode['Point']['pos'].split()))

        return geocode_pos

    @classmethod
    def get_features(cls, response: requests.Response) -> list:
        json_response = \
            response.json()['response']['GeoObjectCollection']['featureMember']
        return json_response
