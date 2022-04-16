from flask_wtf import FlaskForm
from sqlalchemy_serializer import SerializerMixin


class Model(SerializerMixin):
    def load_fields(self, source: FlaskForm or dict):
        """
        Функция загружает поля для данной таблицы

        :param source: источник, из которого нужно брать поля,
        тип данных - flask_wtf.FlaskForm или dict
        :return: self
        :raises: TypeError: неверный тип source
        """

        if isinstance(source, dict):
            for key in source:
                self.__setattr__(key, source[key])

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

        else:
            raise TypeError('Неверный тип source')

        # Все прошло успешно, возвращаем себя
        return self

    @staticmethod
    def find_fields(session, model, columns: list, value) -> list or None:
        """
        Поиск полей в таблице по нескольким колонкам

        :param model: модель, в таблице которой, нужно искать
        :param columns: названия колонок, по которым нужно искать.
        Их порядок важен, так как функция возвращает первые попавшиеся значения
        :param value: искомое значение
        :return: список моделей, в случае нахождения или None
        """
        for column in columns:
            fields = session.query(model).filter(
                getattr(model, column) == value).all()
            if len(fields) > 0:
                return fields
