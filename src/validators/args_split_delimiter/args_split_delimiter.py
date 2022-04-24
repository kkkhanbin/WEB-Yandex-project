from src.validators.validator import Validator


class ArgsSplitDelimiter(Validator):
    """
    Валидатор, предназначенный для проверки строки

    При валидации получает строку, далее разделяет ее с помощью метода
    split(delimiter), сравнивает длину полученного списка со своим значением
    req_len и проверяет тип каждого элемента на присутствие в списке types
    """

    # Сообщения ошибок
    INCORRECT_LENGTH_MESSAGE = 'Неверная длина аргумента'
    INCORRECT_ELEMENT_TYPE_MESSAGE = 'Неверный тип значения {element}'
    NOT_IN_RANGE_MESSAGE = \
        'Число {number} не находится в диапазоне от {min_border} до ' \
        '{max_border}'

    def __init__(
            self, types: list = None, length: int = 2, delimiter: str = ',',
            min_border: int = 0, max_border: int = 100,
            *args, **kwargs):
        """
        :param types: список возможных типов строки
        :param length: требуемая длина списка после деления по параметру
        delimiter
        :param delimiter: разделитель строки
        :param min_border: нижняя граница каждого числа
        :param max_border: верхняя граница каждого числа
        """

        if types is None:
            types = []

        self.types = types
        self.length = length
        self.delimiter = delimiter
        self.min_border = min_border
        self.max_border = max_border

        super().__init__(*args, **kwargs)

    def __call__(self, *args):
        super().__call__(*args)

        # Проверяемое значение
        check_string = self.get_validation_data(*args)

        # Проверка на неправильное значение
        if not isinstance(check_string, str):
            self.stop_validation(self.INCORRECT_TYPE_MESSAGE)

        check_string = check_string.split(self.delimiter)

        # Проверка длины строки после ее деления
        if len(check_string) != self.length:
            self.stop_validation(self.INCORRECT_LENGTH_MESSAGE)

        # Проходим по каждому элементу строки
        for element in check_string:

            # Проверка каждого типа из списка возможных типов
            for el_type in self.types:
                try:
                    el_type(element)
                except TypeError:
                    self.stop_validation(
                        self.INCORRECT_ELEMENT_TYPE_MESSAGE.format(
                            element=element))

                if not (self.min_border <=
                        el_type(element) <=
                        self.max_border):
                    self.stop_validation(self.NOT_IN_RANGE_MESSAGE.format(
                        number=element, min_border=self.min_border,
                        max_border=self.max_border))
