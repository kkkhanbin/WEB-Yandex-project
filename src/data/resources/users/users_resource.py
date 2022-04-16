from flask_restful import reqparse, abort

from ..resource import RestResource
from src.data import session
from src.data.models import User
from src.forms.validators import Unique, ArgumentValidator


class UsersResource(RestResource):
    @staticmethod
    def add_arguments(parser: reqparse.RequestParser) -> None:
        parser.add_argument('id', required=False, type=int)
        parser.add_argument('nickname', required=True, )
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('surname', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('countries', required=False, type=list)

    @staticmethod
    def get_user(login) -> User:
        user = User.find(session, login)
        if user is None:
            abort(404, message=f'User {login} not found')
        return user
