from abc import ABC

from wtforms.validators import StopValidation


class Validator(ABC):
    """
    Кастомный валидатор полей форм или простых значений

    Все валидаторы никак не меняют передаваемое значение при валидации
    """

    # Типы объектов валидации
    VALIDATION_FIELD_TYPE = 'field'
    VALIDATION_ARGUMENT_TYPE = 'argument'

    # Сообщения ошибок
    DEFAULT_VALIDATION_ERROR_MESSAGE = 'Произошла ошибка при валидации'
    INCORRECT_TYPE_MESSAGE = 'Неверный тип аргумента'

    def __init__(self, message=None, type=VALIDATION_FIELD_TYPE):
        """
        Инициализация валидатора

        :param message: сообщение, которое будет выводится при провале на
        валидации
        :param type: тип валидируемых значений, возможные варианты: field -
        для валидации поля из формы и argument - для аргумента из парсера
        """

        self.message = message
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
        validation_data = args[1].data \
            if self.type == self.VALIDATION_FIELD_TYPE else args[0]
        return validation_data

    def stop_validation(self, message: str = None):
        if self.message is None:
            message = self.DEFAULT_VALIDATION_ERROR_MESSAGE

        raise StopValidation(message)
