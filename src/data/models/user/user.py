import os

from flask_wtf import FlaskForm
from flask_login import UserMixin

from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import Column, Integer, String

from src.config.constants import AVATAR_PATH, PROFILE_PATH
from src.data.db_session import SqlAlchemyBase
from src.data.models.model import Model
from src.data.models.use_files import UseFiles


class User(Model, UseFiles, SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    # Таблица
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    access_level = Column(Integer, server_default='0', nullable=False)

    # Доступные уровни доступа ключей для уровней доступа пользователей
    ACCESS_LEVELS_TO_APIKEY = {
        0: [0],
        1: [0, 1]
    }

    # Логин-колонки
    LOGIN_COLUMNS = ['id', 'nickname', 'email']

    @property
    def apikey_access_levels(self) -> list:
        return self.ACCESS_LEVELS_TO_APIKEY[self.access_level]

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
            self.save_image(data, os.path.join(
                *AVATAR_PATH).format(profile_id=self.id))

    def load_fields(self, source: FlaskForm or dict, hash_password=True):
        # Хеширование пароля
        if hash_password:
            if isinstance(source, FlaskForm):
                source.password.data = generate_password_hash(
                    source.password.data)
            elif isinstance(source, dict):
                source['password'] = generate_password_hash(source['password'])

        super().load_fields(source)

    @classmethod
    def find(cls, session, key):
        return super()._find(session, key, *cls.LOGIN_COLUMNS)

    @property
    def profile_path(self) -> str:
        profile_path = os.path.join(*PROFILE_PATH).format(
            profile_id=self.id)
        return profile_path

    def create_profile_dirs(self) -> None:
        self.create_dir(self.profile_path)

    def delete_profile_dirs(self) -> None:
        self.delete_file(self.profile_path)
