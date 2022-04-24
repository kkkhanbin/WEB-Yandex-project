from src.validators.validator import Validator


class Range(Validator):
    """
    Валидатор, предназначенный для того, чтобы проверить, находится ли число в
    заданном диапазоне
    """

    # Сообщения ошибок
    NOT_IN_RANGE_MESSAGE = \
        'Число {number} не находится в диапазоне от {min_border} до ' \
        '{max_border}'

    def __init__(
            self, min_border: int = 0, max_border: int = 100, *args, **kwargs):
        """
        :param min_border: нижняя граница
        :param max_border: верхняя граница
        """

        self.min_border = min_border
        self.max_border = max_border

        super().__init__(*args, **kwargs)

    def __call__(self, *args):
        super().__call__(*args)

        # Проверяемое значение
        number = self.get_validation_data(*args)

        try:
            number = float(number)
        except TypeError:
            self.stop_validation(self.INCORRECT_TYPE_MESSAGE)

        if not (self.min_border <= number <= self.max_border):
            self.stop_validation(self.NOT_IN_RANGE_MESSAGE.format(
                number=number, min_border=self.min_border,
                max_border=self.max_border))
