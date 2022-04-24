from ..resource import RestResource
from src.data import session
from src.data.models import User
from src.parsers import UserDataParser
from src.data.models.validators import ModelNotFound


class UsersResource(RestResource):
    USER_DATA_PARSER_ID = 'user_data'

    def __init__(self):
        super().__init__()

        self.parsers[self.USER_DATA_PARSER_ID] = UserDataParser()

    @staticmethod
    def get_user(login) -> User:
        user = User.find(session, login)
        User.validate(ModelNotFound(user, 'Такого пользователя не существует'))
        return user

    def get_user_data(self, user_id: int = None, **except_values):
        if except_values or user_id is not None:
            parser = UserDataParser(user_id, except_values)
            return parser.parse_args()
        else:
            return self.parsers[self.USER_DATA_PARSER_ID].parse_args()
