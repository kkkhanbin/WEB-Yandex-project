from wtforms.validators import StopValidation

from src.forms.validators.validator import Validator
from src.data import session


class Unique(Validator):
    def __init__(self, model, message=None, except_values:list=None):
        if except_values is None:
            except_values = []

        self.except_values = except_values
        self.model = model
        self.message = message
        self.field_flags = {'required': True}

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

        # Здесь мы ищем значение совпадения в колонке column_name, где
        # значения колонки равны переданному значению field.data
        matches = session.query(self.model).filter(
            getattr(self.model, column_name) == field.data).all()

        # Проверка на то, есть ли все совпадения в except-списке. Если хотя-бы
        # одно совпадение не в списке, то passed станет False
        passed = True
        for match in matches:
            if getattr(match, column_name) not in self.except_values:
                passed = False
                break

        # Если все совпадения в except-списке. Если совпадений не было найдено,
        # то passed тоже будет True, поэтому нет смысла делать доп. проверку на
        # отсутствие совпадений
        if passed:
            return

        message = f'Поле {column_name} уже существует' \
            if self.message is None else self.message

        field.errors[:] = []
        raise StopValidation(message)
