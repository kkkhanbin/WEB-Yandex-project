from flask_wtf import FlaskForm
from sqlalchemy_serializer import SerializerMixin


class Model(SerializerMixin):
    UNAUTHORIZED_DESCRIPTION = 'Вы не авторизованы'
    INCORRECT_SOURCE_TYPE_MESSAGE = 'Неверный тип source'

    def load_fields(self, source: FlaskForm or dict):
        """
        Функция загружает поля для данной таблицы

        :param source: источник, из которого нужно брать поля,
        тип данных - flask_wtf.FlaskForm или dict
        :return: self
        :raises: TypeError: неверный тип source
        """

        # Парсинг словаря
        if isinstance(source, dict):
            # Пробегаемся по ключу в словаре
            for key in source:
                self.__setattr__(key, source[key])

        # Парсинг flask-формы
        elif isinstance(source, FlaskForm):
            # Проходим по названиям колонок таблицы
            for column_name in self.__table__.columns.keys():
                # Получение самой колонки
                column = type(self).__dict__[column_name]

                # Если автоинкремент выключен
                if column.autoincrement == 'auto':
                    # Если в форме есть такое поле
                    if column_name in source.__dict__:
                        self.__setattr__(
                            column_name,
                            source.__getattribute__(column_name).data)

        # Неверный тип источника
        else:
            raise TypeError(self.INCORRECT_SOURCE_TYPE_MESSAGE)

        # Все прошло успешно, возвращаем себя
        return self

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
        if model is None:
            model = cls

        for column_name, column_value in columns.items():
            fields = session.query(model).filter(
                getattr(model, column_name) == column_value).all()
            if len(fields) > 0:
                return fields

        return []
