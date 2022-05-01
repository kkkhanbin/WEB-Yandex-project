import uuid

from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from src.data.db_session import SqlAlchemyBase
from src.data.models.model import Model
from src.config.utils import default


class Apikey(Model, SqlAlchemyBase):
    __tablename__ = 'apikeys'

    # Таблица
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    apikey = Column(String, nullable=False, unique=True)
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)
    access_level = Column(Integer, nullable=False, server_default='0')
    block = Column(Boolean, nullable=False, server_default='0')

    # Сообщения ошибок
    BLOCKED_MESSAGE = 'Этот API-ключ заблокирован. Его нельзя редактировать'

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
        owner = default(owner, current_user)

        if isinstance(source, FlaskForm):
            if load_apikey:
                source.apikey.data = self.create_apikey()
            if load_owner:
                source.owner.data = owner.id
        elif isinstance(source, dict):
            if load_apikey:
                source['apikey'] = self.create_apikey()
            if load_owner:
                source['owner'] = owner.id

        return super().load_fields(source)

    @classmethod
    def find(cls, session, key):
        return super()._find(session, key, 'id', 'owner', 'apikey')
