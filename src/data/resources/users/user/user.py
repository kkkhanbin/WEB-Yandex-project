import logging

from flask import jsonify

from src.data.resources.users.users_resource import UsersResource
from src.data import session


class UserResource(UsersResource):
    def get(self, login):
        logging.info(f'Был прислан GET-запрос на получение пользователя '
                     f'по логину {login}')

        self.get_apikey()
        user = self.get_user(login)

        return jsonify({'user': user.to_dict(
            only=('id', 'surname', 'name', 'nickname', 'email'))})

    def delete(self, login):
        logging.info(f'Был прислан DELETE-запрос на удаление пользователя '
                     f'по логину {login}')

        self.get_apikey(1)

        user = self.get_user(login)
        session.delete(user)
        session.commit()

        return jsonify({'success': 'OK'})

    def put(self, login):
        logging.info(f'Был прислан PUT-запрос на обновление пользователя '
                     f'по логину {login}')

        self.get_apikey(1)
        user = self.get_user(login)

        # Преобразование всех значений в словаре в список с этими же значениями
        user_data = user.to_dict()
        for key in user_data:
            user_data[key] = [user_data[key]]

        # Парсинг реквеста с данными пользователя
        user_data = self.get_user_data(user.id, **user_data)
        user_data.id = user.id

        user.load_fields(user_data)
        session.commit()

        return jsonify({'success': 'OK'})
