from flask import jsonify

from ..users_resource import UsersResource
from src.data import session


class UserResource(UsersResource):
    def get(self, login):
        user = self.get_user(login)
        return jsonify({'user': user.to_dict(
            only=('surname', 'name', 'nickname', 'email'))})

    def delete(self, login):
        user = self.get_user(login)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, login):
        user = self.get_user(login)
        user.load_fields(self.parser.parse_args())
