import os

from PIL import Image

from flask import abort
from flask_wtf import FlaskForm
from flask_login import UserMixin, current_user

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import NotFound, Unauthorized, Forbidden

from sqlalchemy import Column, Integer, String

from src.config.constants import AVATAR_PATH
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
    access_level = Column(Integer, server_default='0', nullable=False)

    NOT_FOUND_DESCRIPTION = 'Пользователь не найден'
    FORBIDDEN_DESCRIPTION = 'У вас нет доступа к этому пользователю'

    DEFAULT_VALIDATE_EXCEPTIONS = [NotFound, Forbidden, Unauthorized]

    ACCESS_LEVELS_TO_APIKEY = {
        0: [0],
        1: [0, 1]
    }

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
            self.create_dir(self)
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
    def find(cls, session, login):
        """
        Поиск пользователя по нескольким колонкам

        Является упрощением функции find_fields для поиска пользователя.
        Благодаря этой функции, можно менять порядок колонок для поиска
        пользователя

        :param session: БД сессия
        :param login: искомое значение колонки
        :return: User, если пользователь найден, иначе - None
        :raises: werkzeug.exceptions.HTTPException
        """

        # Поиск пользователя по колонкам id, nickname, email
        response = cls.find_fields(
            session, User, id=login, nickname=login, email=login)

        # Если мы ничего не нашли
        if len(response) == 0:
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

    @classmethod
    def validate(
            cls, user: SqlAlchemyBase, check_user: SqlAlchemyBase = None,
            validators: list = None):
        """
        Проверка доступа пользователя-check_user к профилю пользователя-user

        :param user: пользователь, к которому будет проверяться доступ
        :param check_user: проверяемый пользователь (подразумевается что будет
        использоваться текущий, поэтому он и стоит по умолчанию)
        :param validators: список валидаторов на проверку, по умолчанию
        каждый валидатор в списке. В данном случае, валидатор -
        werkzeug.exceptions.HTTPException.
        См. Model.DEFAULT_VALIDATE_EXCEPTIONS
        :raises: werkzeug.exceptions.HTTPException - в случае если доступ к
        профилю запрещен
        """

        # Значения по умолчанию
        if check_user is None:
            check_user = current_user
        if validators is None:
            validators = cls.DEFAULT_VALIDATE_EXCEPTIONS

        # Первым делом нужно проверить авторизован ли пользователь
        if Unauthorized in validators and not check_user.is_authenticated:
            abort(Unauthorized.code, description=cls.UNAUTHORIZED_DESCRIPTION)

        # Если такого профиля не существует
        if NotFound in validators and user is None:
            abort(NotFound.code, description=cls.NOT_FOUND_DESCRIPTION)

        # Если это не одинаковые профили
        if Forbidden in validators and \
                not check_user.check_login(user.nickname):
            abort(Forbidden.code, description=cls.FORBIDDEN_DESCRIPTION)
