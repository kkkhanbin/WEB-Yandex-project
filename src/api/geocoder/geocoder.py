import requests

from src.api.api import UseApikey


class Geocoder(UseApikey):
    URL = 'http://geocode-maps.yandex.ru/1.x/'

    def get(self, params: dict = None, headers: dict = None) \
            -> requests.Response:
        params['format'] = 'json' \
            if 'format' not in params else params['format']

        return super().get(params=params, headers=headers)

    @classmethod
    def get_pos(cls, response: requests.Response) -> tuple or None:
        if not response:
            return 0, 0

        features = cls.get_features(response)

        if len(features) == 0:
            return 0, 0

        geocode = features[0]['GeoObject']
        geocode_pos = tuple(map(float, geocode['Point']['pos'].split()))

        return geocode_pos

    @classmethod
    def get_features(cls, response: requests.Response) -> list:
        if not response:
            return []

        json_response = \
            response.json()['response']['GeoObjectCollection']['featureMember']
        return json_response
