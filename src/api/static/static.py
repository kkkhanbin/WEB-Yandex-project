from src.api.api import Api, UseApikey


class Static(UseApikey, Api):
    URL = 'http://static-maps.yandex.ru/1.x/'
