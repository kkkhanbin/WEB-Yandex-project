import logging

from flask import jsonify

from src.data.resources.users.users_resource import UsersResource
from src.data import session
from src.data.models import User


class UsersListResource(UsersResource):
    def get(self):
        logging.info(
            'Был прислан GET-запрос на получение списка пользователей')

        self.get_apikey()
        users = session.query(User).all()

        users_data = [
            user.to_dict(only=('id', 'surname', 'name', 'nickname', 'email'))
            for user in users]

        return jsonify({'users': users_data})

    def post(self):
        logging.info(
            'Был прислан POST-запрос на добавление пользователя')

        self.get_apikey(1)

        user = User()
        user_data = self.get_user_data()
        user.load_fields(user_data)

        session.add(user)
        session.commit()

        return jsonify({'success': 'OK'})
