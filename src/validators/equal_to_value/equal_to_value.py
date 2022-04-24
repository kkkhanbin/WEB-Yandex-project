from src.validators.validator import Validator


class EqualToValue(Validator):
    """
    Валидатор, предназначенный для проверки равенства значения аргумента
    какому-либо значению
    """

    # Сообщения ошибок
    NOT_EQUAL_MESSAGE = \
        'Значение {validation_value} не равно нужному значению {equal_value}'

    def __init__(self, equal_value, *args, **kwargs):
        """
        Инициализация валидатора равных значений

        :param equal_value: значение, которому должно быть равно валидируемое
        значение при валидации
        """

        self.equal_value = equal_value

        super().__init__(*args, **kwargs)

    def __call__(self, *args):
        """
        Процесс валидации, сравнение значение происходит с помощью оператора ==
        """

        super().__call__(*args)

        # Проверяемое значение
        validation_data = self.get_validation_data(*args)

        # Если проверяемое значение не равно нужному значению, то валидация
        # провалена
        if validation_data != self.equal_value:
            self.stop_validation(self.NOT_EQUAL_MESSAGE.format(
                validation_value=validation_data,
                equal_value=self.equal_value))
