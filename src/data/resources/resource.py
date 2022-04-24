from flask_restful import Resource

from src.data.models import Apikey
from src.data import session
from src.data.models.validators import ModelNotFound, AccessLevel
from src.parsers import ApikeyParser


class RestResource(Resource):
    APIKEY_PARSER_ID = 'apikey'

    def __init__(self):
        self.parsers = {}

        self.parsers[self.APIKEY_PARSER_ID] = ApikeyParser()

    def get_apikey(self, access_level: int = 0) -> str:
        """
        Получение API-ключа в реквесте и его валидация

        :return: API-ключ из реквеста
        """

        req_apikey = self.parsers[self.APIKEY_PARSER_ID].parse_args().apikey
        apikey = Apikey.find(session, req_apikey)
        Apikey.validate(
            ModelNotFound(apikey, 'Такого API-ключа не существует'),
            AccessLevel(
                apikey, access_level, 'У вашего API-ключа не хватает доступа'))

        return apikey
