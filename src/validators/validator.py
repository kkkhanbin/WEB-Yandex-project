from abc import ABC

from flask_wtf import FlaskForm
from wtforms.validators import StopValidation

from src.config.utils import default


class Validator(ABC):
    """
    Кастомный валидатор полей форм или простых значений

    Все валидаторы никак не меняют передаваемое значение при валидации
    """

    # Сообщения ошибок
    DEFAULT_VALIDATION_ERROR_MESSAGE = 'Произошла ошибка при валидации'
    INCORRECT_TYPE_MESSAGE = 'Неверный тип аргумента'

    def __init__(self, message=None):
        """
        Инициализация валидатора

        :param message: сообщение, которое будет выводится при провале на
        валидации
        :param type: тип валидируемых значений, возможные варианты: field -
        для валидации поля из формы и argument - для аргумента из парсера
        """

        self.message = default(message, self.DEFAULT_VALIDATION_ERROR_MESSAGE)
        self.type = type

        self.field_flags = {'required': True}

    def __call__(self, *args):
        """
        Процесс валидации

        Для типа валидируемого объекта - field:
            :param form: Форма для валидации, тип - flask_wtf.FlaskForm
            :param field: Поле для валидации, тип - wtforms.Field
            :return: None, в случаях, когда валидация прошла успешно
            :raises: wtforms.validators.StopValidation, в случаях, когда была
            найдена ошибка при валидации

        Для типа валидируемого объекта - argument:
            :param argument: значение аргумента, который парсеры передают
            типам при конвертации
        """

        pass

    def get_validation_data(self, *args):
        if isinstance(args[0], FlaskForm):
            return args[1].data
        return args[0]

    def stop_validation(self, message: str = None):
        message = default(message, self.message)
        raise StopValidation(message)
