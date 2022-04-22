from src.api.api import Api, UseApikey


class Static(Api, UseApikey):
    URL = 'http://static-maps.yandex.ru/1.x/'
