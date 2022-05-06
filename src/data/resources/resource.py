from flask_restful import Resource

from src.data.models import Apikey, ModelNotFound, AccessLevel
from src.data import session
from src.parsers import ApikeyParser


class RestResource(Resource):
    APIKEY_PARSER_ID = 'apikey'

    # Сообщения ошибок
    APIKEY_NOT_FOUND_MESSAGE = 'Такого API-ключа не существует'
    APIKEY_ACCESS_FORBIDDEN_MESSAGE = 'У вашего API-ключа не хватает доступа'

    def __init__(self):
        self.parsers = {self.APIKEY_PARSER_ID: ApikeyParser()}

    def get_apikey(self, access_level: int = 0) -> str:
        """
        Получение API-ключа в реквесте и его валидация

        :return: API-ключ из реквеста
        """

        req_apikey = self.parsers[self.APIKEY_PARSER_ID].parse_args().apikey
        apikey = Apikey.find(session, req_apikey)
        Apikey.validate(
            ModelNotFound(apikey, self.APIKEY_NOT_FOUND_MESSAGE),
            AccessLevel(
                apikey, access_level, self.APIKEY_ACCESS_FORBIDDEN_MESSAGE))

        return apikey
