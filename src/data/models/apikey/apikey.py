import uuid

from flask import abort
from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from werkzeug.exceptions import Forbidden, NotFound, Unauthorized

from src.data.db_session import SqlAlchemyBase
from src.data.models.model import Model


class Apikey(Model, SqlAlchemyBase):
    __tablename__ = 'apikeys'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    apikey = Column(String, nullable=False, unique=True)
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)
    access_level = Column(Integer, nullable=False, server_default='0')
    block = Column(Boolean, nullable=False, server_default='0')

    NOT_FOUND_DESCRIPTION = 'API-ключ не найден'
    FORBIDDEN_DESCRIPTION = 'У вас нет доступа к этому API-ключу'

    DEFAULT_VALIDATE_EXCEPTIONS = [NotFound, Forbidden, Unauthorized]

    def check_apikey(self, apikey: str) -> bool:
        """
        Функция для проверки переданного API-ключа на соответствие с
        API-ключом данной модели

        :param apikey: проверяемый API-ключ
        :return bool: в случае соответствия - True, иначе - False
        """

        return apikey == self.apikey

    def create_apikey(self) -> str:
        """
        Функция для создания API-ключей

        :return: уникальный идентификатор ключа
        """

        return str(uuid.uuid4())

    def load_fields(
            self, source: FlaskForm or dict, owner=None, load_apikey=True,
            load_owner=True):
        if owner is None:
            owner = current_user

        if isinstance(source, FlaskForm):
            if load_apikey:
                source.apikey = Column(String)
                source.apikey.data = self.create_apikey()
            if load_owner:
                source.owner = Column(Integer)
                source.owner.data = owner.id
        elif isinstance(source, dict):
            if load_apikey:
                source['apikey'] = self.create_apikey()
            if load_owner:
                source['owner'] = owner.id

        super().load_fields(source)

    @classmethod
    def validate(
            cls, apikey: SqlAlchemyBase, user=None, validators: list = None):
        """
        Проверка доступа пользователя-user к API-ключу-apikey_id

        :param apikey: модель Apikey, к которой нужно проверить доступ
        :param user: проверяемый пользователь, по умолчанию стоит текущий
        :param validators: список валидаторов на проверку, по умолчанию
        каждый валидатор в списке. В данном случае, валидатор -
        werkzeug.exceptions.HTTPException.
        См. Model.DEFAULT_VALIDATE_EXCEPTIONS
        :raises: werkzeug.exceptions.HTTPException - в случае если доступ к
        API-ключу запрещен или что-то пошло не так
        """

        # Значения по умолчанию
        if user is None:
            user = current_user
        if validators is None:
            validators = cls.DEFAULT_VALIDATE_EXCEPTIONS

        # Первым делом нужно проверить авторизован ли пользователь
        if Unauthorized in validators and not user.is_authenticated:
            abort(Unauthorized.code, description=cls.UNAUTHORIZED_DESCRIPTION)

        # Если такого API-ключа не существует
        if NotFound in validators and (apikey is None or apikey == []):
            abort(NotFound.code, description=cls.NOT_FOUND_DESCRIPTION)

        if isinstance(apikey, list):
            apikey = apikey[0]

        # Если создатель API-ключа не пользователь
        if Forbidden in validators and apikey.owner != user.id:
            abort(Forbidden.code, description=cls.FORBIDDEN_DESCRIPTION)
