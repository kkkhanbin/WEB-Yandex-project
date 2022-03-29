from wtforms.validators import StopValidation

from src.forms.validators.validator import Validator
from src.data import session


class Unique(Validator):
    def __init__(self, model, message=None):
        self.model = model
        self.message = message
        self.field_flags = {"required": True}

    def __call__(self, form, field):
        """
        Процесс валидации

        :param form: Форма для валидации, тип - flask_wtf.FlaskForm
        :param field: Поле для валидации, тип - wtforms.Field
        :return: None, в случаях, когда валидация прошла успешно
        :raises: wtforms.validators.StopValidation, в случаях, когда была
        найдена ошибка при валидации
        """

        # Название колонки
        column_name = field.name

        # здесь мы ищем значение из
        # таблицы self.model, где значение field равно значению из
        # колонки field.__name__ и если таких значений нет,
        # значит валидация прошла успешно
        if len(session.query(self.model).filter(self.model().__getattribute__(
                column_name) == field.data).all()) == 0:
            return

        message = f'Поле {column_name} уже существует' \
            if self.message is None else self.message

        field.errors[:] = []
        raise StopValidation(message)
