import os

from PIL import Image

from flask import abort
from flask_wtf import FlaskForm
from flask_login import UserMixin

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import NotFound

from sqlalchemy import Column, Integer, String

from src.data.db_session import SqlAlchemyBase
from src.data.models.model import Model


class User(Model, SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    def check_login(self, login: str or int) -> bool:
        """
        Проверяет совпадение логина с логин-колонками своей модели

        :param login: проверяемый логин
        :return: True если найдено совпадение, иначе - False
        """

        # Используется приведение к строке, потому что аргумент login не всегда
        # может быть числом при искомой колонке - id. Например, login - str:256
        # и id - int:256, значения по сути одинаковое, а типы разные. Это
        # добавлено также из-за того, что чаще всего login передается в
        # качестве аргумента в адресной строке, а там, нельзя передавать строки
        # и числа как один параметр
        return str(login) in [str(self.id), self.nickname, self.email]

    def save_avatar_image(self, data) -> None:
        """
        Сохранение фото профиля

        :param data: любые данные фото, которые можно открыть с
        помощью PIL.Image.open
        :return: None
        """

        if data:
            self.create_dir(self)
            self.save_image(data, os.path.join(
                'static', 'upload', 'profiles', str(self.id), 'avatar.png'))

    def load_fields(self, source: FlaskForm or dict):
        source.password.data = generate_password_hash(source.password.data)
        super().load_fields(source)

    @classmethod
    def find(cls, session, login, abort_if_user_not_find: bool=False):
        """
        Поиск пользователя по нескольким колонкам

        Является упрощением функции find_fields для поиска пользователя.
        Благодаря этой функции, можно менять порядок колонок для поиска
        пользователя

        :param session: БД сессия
        :param login: искомое значение колонки
        :param abort_if_user_not_find: создавать ошибку 404 при ненахождении
        пользователя
        :return: User, если пользователь найден, иначе - None
        :raises
        """

        # Поиск пользователя по колонкам id, nickname, email
        response = cls.find_fields(
            session, User, ['id', 'nickname', 'email'], login)

        # Если мы ничего не нашли
        if response is None:
            # Если нужно создавать ошибку 404
            if abort_if_user_not_find:
                abort(NotFound.code,
                      description=f'Пользователь {login} не найден')
            # Если не нужно (тут можно не ставить else, но так удобнее читать)
            else:
                return None
        # Если что-то нашли (тут тоже можно не ставить else)
        else:
            # То просто возвращаем найденного пользователя
            return response[0]

    @staticmethod
    def create_dir(user) -> None:
        """
        Создание директории для файлов пользователя

        :param user: пользователь, которому нужно создать директорию
        :return: None
        """

        upload_path = os.path.join(
            'static', 'upload', 'profiles', str(user.id))
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

    @staticmethod
    def save_image(data, destiny: str) -> None:
        """
        Сохранение фотографии

        Пришлось прибегнуть к способу через библиотеку PIL, так как встроенный
        во flask метод data.save() работал неккоректно, т.е. изображение
        сохранялось побитым и ни я, ни flask не могли его открыть

        :param data: любые данные фото, которые можно открыть через
        PIL.Image.open()
        :param destiny: путь до сохраняемого файла
        :return: None
        """

        img = Image.open(data)
        img.save(destiny)
