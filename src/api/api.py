from abc import ABC

import requests
import urllib


class Api(ABC):
    """
    Класс для взаимодействия с другими API
    """

    def get(self, params: dict = None, headers: dict = None) \
            -> requests.Response:
        """
        Получение результата GET-запроса на URL API-класса

        :param dict params: параметры адресной строки. По умолчанию пустой
        :param dict headers: заголовки адресной строки. По умолчанию пустой
        :return: request.Response
        """

        params = {} if params is None else params
        headers = {} if headers is None else headers

        return requests.get(self.URL, params=params, headers=headers)

    @classmethod
    def create_url(cls, url=None, params: dict = None) -> str:
        params = {} if params is None else params
        url = cls.URL if url is None else url

        return '?'.join([url, urllib.parse.urlencode(params)])


class UseApikey(ABC):
    """
    Класс для тех, кто использует API-ключ при запросах и наследуется от
    класса src.data.api.Api
    """

    def __init__(self, apikey: str, *args, **kwargs):
        self.apikey = apikey

        super().__init__(*args, **kwargs)

    def get(self, params: dict = None, headers: dict = None) \
            -> requests.Response:
        params = {} if params is None else params
        params['apikey'] = self.apikey

        return super().get(params, headers)
