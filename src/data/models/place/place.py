import os

from flask import abort
from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from werkzeug.exceptions import RequestEntityTooLarge

from src.config.constants import PLACE_MEDIA_FILES_PATH, MAX_PLACE_MEDIA_SIZE
from src.data.db_session import SqlAlchemyBase
from src.data.models.model import Model
from src.data.models.use_files import UseFiles
from src.data.models import User
from src.api import Geocoder
from src.data.models.validators import OwnerToModel, UserToUser, \
    UserUnauthorized, ModelNotFound


class Place(Model, UseFiles, SqlAlchemyBase):
    __tablename__ = 'places'

    # Таблица
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String, nullable=True)
    name = Column(String, nullable=True)
    lon = Column(Float, nullable=True)
    lat = Column(Float, nullable=True)

    @classmethod
    def find(cls, session, key):
        return super()._find(session, key, 'id', 'owner', 'name')

    def load_fields(self, owner=None, *args, **kwargs):
        source = args[0]
        owner = current_user if owner is None else owner

        owner_id = owner.id
        ll = Geocoder.get_pos(Geocoder.get({'geocode': source.name.data}))
        if ll is None:
            ll = None, None

        columns = [('lon', ll[0]), ('lat', ll[1]), ('owner', owner_id)]
        for key, value in columns:
            if isinstance(source, FlaskForm):
                setattr(getattr(source, key), 'data', value)
            elif isinstance(source, dict):
                source[key] = value

        return super().load_fields(*args, **kwargs)

    def save_place_media(self, data, user_id) -> None:
        data = [data] if not isinstance(data, list) else data

        for file in data:
            if not file.filename:
                # Если название файла пустое, его нельзя сохранить.
                # Такое случается когда передали пустой FileStorage
                continue

            filename = self.secure_path(file.filename)
            media_path = os.path.join(*PLACE_MEDIA_FILES_PATH).format(
                profile_id=user_id, place_id=self.id)
            path = os.path.join(media_path, filename)

            if self.get_size(media_path) > MAX_PLACE_MEDIA_SIZE:
                abort(
                    RequestEntityTooLarge.code,
                    description=f'Размер вашего хранилища слишком большой. Ма'
                                f'ксимальный размер - {MAX_PLACE_MEDIA_SIZE}')

            # Создание директория для вложенных папок
            self.create_dir(
                os.path.join(media_path, *os.path.split(filename)[:-1]))

            file.save(path)

    @staticmethod
    def get_place_media_path(user, place) -> str:
        media_path = os.path.join(
            *PLACE_MEDIA_FILES_PATH).format(
            profile_id=user.id, place_id=place.id)
        return media_path

    @classmethod
    def get_view_config(cls, session, login, place_id, path=None) -> tuple:
        """
        Получение шаблонных конфигурации для просмотра посещенного места

        :param session: сессия БД
        :param login: логин пользователя
        :param place_id: id места
        :param path: путь до файла в директории места
        :return tuple: user, place, file_path, media_path, path если указан
        path, иначе user, place
        """

        # Пользователь
        user = User.find(session, login)
        User.validate(UserUnauthorized(), ModelNotFound(user),
                      UserToUser(user))

        # Место
        place = Place.find(session, place_id)
        Place.validate(ModelNotFound(place), OwnerToModel(place))

        if path is not None:
            # Убираем точки из пути чтобы пользователь не мог посмотреть за
            # свою папку
            path = Place.secure_path(path)

            # Путь до файла
            media_path = cls.get_place_media_path(user, place)
            file_path = media_path
            if path:
                file_path = os.path.join(file_path, path)

            return user, place, file_path, media_path, path
        else:
            return user, place
