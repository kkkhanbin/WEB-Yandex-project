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
            for column_name in self.__table__.columns.keys():
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

        # Все прошло успешно, возвращем себя
        return self
