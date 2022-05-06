import logging

from flask import abort
from werkzeug.exceptions import BadRequest
from flask_wtf import FlaskForm
from flask_restful.reqparse import Namespace
from wtforms import Field
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.exc import OperationalError, IntegrityError

from src.config.utils import default


class Model(SerializerMixin):
    # Сообщения
    INCORRECT_SOURCE_TYPE_MESSAGE = 'Неверный тип source'
    INCORRECT_ACTION_MESSAGE = 'Неверный тип действия над моделью'
    MODIFY_MODEL_ERROR = 'Возникла ошибка при внесении изменений. ' \
                         'Перепроверьте корректность данных'

    # Типы действий для изменения модели
    ADD_MODEL = 'add'
    EDIT_MODEL = 'edit'
    DELETE_MODEL = 'delete'
    MODEL_ACTIONS = [ADD_MODEL, EDIT_MODEL, DELETE_MODEL]

    def load_fields(self, source: FlaskForm or dict or Namespace):
        """
        Функция загружает поля для данной таблицы

        :param source: источник, из которого нужно брать поля,
        тип данных - flask_wtf.FlaskForm, dict или Namespace
        :return: self
        :raises: TypeError: неверный тип source
        """

        source = self.convert_in_dict(source)

        # Загрузка полей из словаря
        for column_name in source:
            # Если проверяемое поле - одна из колонок таблицы
            if column_name in self.__table__.columns.keys():
                setattr(self, column_name, source[column_name])

        # Все прошло успешно, возвращаем себя
        return self

    @classmethod
    def convert_in_dict(cls, source: FlaskForm or dict or Namespace):
        source_dict = {}

        # Парсинг Namespace
        if isinstance(source, Namespace):
            source_dict = dict(source)

        # Парсинг словаря
        elif isinstance(source, dict):
            source_dict = source

        # Парсинг flask-формы
        elif isinstance(source, FlaskForm):
            # Конвертирование полей формы из Field в Field.data и в обычный
            # словарь
            for column_name in source.__dict__:
                column = getattr(source, column_name)
                if isinstance(column, Field):
                    source_dict[column_name] = column.data

        # Неверный тип источника
        else:
            raise TypeError(cls.INCORRECT_SOURCE_TYPE_MESSAGE)

        return source_dict

    @classmethod
    def find_fields(cls, session, model=None, **columns) -> list:
        """
        Поиск полей в таблице по нескольким колонкам

        Важен порядок указания колонок, функция идет по колонкам и
        возвращает первые попавшиеся совпадения

        :param session: сессия БД
        :param model: модель, в таблице которой, нужно искать
        :param columns: колонки по которым нужно осуществлять поиск,
        ключ - название колонки, значение - искомое значение колонки.
        Функция ищет строки, где название колонки = ключу и
        ее значение = значению
        :return list: список найденных моделей
        """
        model = default(model, cls)

        for column_name, column_value in columns.items():
            fields = session.query(model).filter(
                getattr(model, column_name) == column_value).all()
            if len(fields) > 0:
                return fields

        return []

    @classmethod
    def _find(cls, session, key, *column_names):
        """
        Поиск поля по нескольким колонкам

        Является упрощением функции find_fields. Благодаря этой функции, можно
        менять порядок и сами колонки для поиска. Рассчитывается, что в
        дочерних классах эта функция будет переопределяться, но это не
        обязательно

        :param session: БД сессия
        :param key: искомое значение колонки
        :param columns: названия колонок
        :return: Model, если поле найдено, list - если найдено несколько
        объектов, иначе - None
        """

        # Конвертирование названий колонок в словарь для функции find_fields
        columns = {}
        for column_name in column_names:
            columns[column_name] = key

        # Поиск по переданным колонкам
        response = cls.find_fields(session, cls, **columns)

        # Если мы ничего не нашли
        if len(response) == 0:
            return None

        # Если найденных моделей больше 1
        elif len(response) > 1:
            return response

        # Если найдена всего одна модель
        return response[0]

    @classmethod
    def validate(cls, *validators: callable) -> None:
        """
        Валидация модели

        Проходит по каждому валидатору в списке, если передан один из
        аргументов args или kwargs, то все валидаторы будут инициализироваться
        вместе с этими аргументами до вызова

        :param validators: список валидаторов, которых нужно использовать.
        См. src/data/models/validators или же любой другой вызываемый объект.
        :return: None
        """

        for validator in validators:
            validator()

    @classmethod
    def modify_model(cls, session, action: str, source=None, model=None):
        """
        Добавление, изменение или удаление модели в БД

        :param session: сессия БД
        :param source: источник данных для изменения или добавления модели
        :param action: тип действия. См. Model.MODEL_ACTIONS
        :param model: класс модели, которую нужно добавить или изменить. Для
        добавления по умолчанию стоит текущий класс
        :return: модель, если все прошло успешно или None
        """

        if action not in cls.MODEL_ACTIONS:
            raise ValueError(cls.INCORRECT_ACTION_MESSAGE)

        if action == cls.ADD_MODEL:
            model = default(model, cls)()

        if action in [cls.ADD_MODEL, cls.EDIT_MODEL]:
            model.load_fields(source)

        try:
            if action == cls.ADD_MODEL:
                session.add(model)
            elif action == cls.DELETE_MODEL:
                session.delete(model)
            session.commit()
        except (OperationalError, IntegrityError) as error:
            logging.error(
                f'При модификации {action} модели {model} из источника '
                f'{source} произошла ошибка: {error}')
            session.rollback()
            abort(BadRequest.code, description=cls.MODIFY_MODEL_ERROR)
        else:
            logging.error(
                f'Модификация {action} модели {model} из источника '
                f'{source} прошла успешно')
            return model

    @classmethod
    def add(cls, session, source, model=None):
        model = default(model, cls)
        logging.info(
            f'Начало добавления модели {model} с источником {source}')
        return cls.modify_model(
            session, cls.ADD_MODEL, source=source, model=model)

    @classmethod
    def edit(cls, session, source, model):
        logging.info(
            f'Начало изменения модели {model} с источником {source}')
        return cls.modify_model(
            session, cls.EDIT_MODEL, source=source, model=model)

    @classmethod
    def delete(cls, session, model):
        logging.info(f'Начало удаления модели {model}')
        return cls.modify_model(session, cls.DELETE_MODEL, model=model)
