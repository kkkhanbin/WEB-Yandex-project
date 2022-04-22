import requests

from src.api.api import Api, UseApikey


class Geocoder(Api, UseApikey):
    URL = 'http://geocode-maps.yandex.ru/1.x/'

    @classmethod
    def get_pos(cls, response: requests.Response) -> tuple or None:
        json_response = response.json()
        features = json_response['response']['GeoObjectCollection']\
            ['featureMember']

        if len(features) == 0 or not response:
            return

        geocode = json_response['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']
        geocode_pos = tuple(map(float, geocode['Point']['pos'].split()))

        return geocode_pos
