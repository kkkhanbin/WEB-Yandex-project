from abc import ABC
import urllib
import logging

import requests

from src.config.utils import default


class Api(ABC):
    """
    Класс для взаимодействия с другими API
    """

    def get(self, params: dict = None, headers: dict = None) \
            -> requests.Response or None:
        """
        Получение результата GET-запроса на URL API-класса

        :param dict params: параметры адресной строки. По умолчанию пустой
        :param dict headers: заголовки адресной строки. По умолчанию пустой
        :return: request.Response или None, если не удалось получить ответ
        """

        params, headers = default(params, {}), default(headers, {})

        try:
            logging.info(f'Был отослан GET-запрос по адресу {self.URL}')
            return requests.get(self.URL, params=params, headers=headers)
        except requests.exceptions.ConnectionError as error:
            logging.error(
                f'Произошла ошибка при посыле GET-запроса по адресу '
                f'{self.URL} - {error}')
            return None

    @classmethod
    def create_url(cls, url=None, params: dict = None) -> str:
        params = default(params, {})
        url = cls.URL if url is None else url

        return '?'.join([url, urllib.parse.urlencode(params)])


class UseApikey(Api):
    """
    Класс для тех, кто использует API-ключ при запросах и наследуется от
    класса src.data.api.Api
    """

    def __init__(self, apikey: str, *args, **kwargs):
        self.apikey = apikey

        super().__init__(*args, **kwargs)

    def get(self, params: dict = None, headers: dict = None) \
            -> requests.Response:
        params = default(params, {})
        params['apikey'] = self.apikey

        return super().get(params, headers)
