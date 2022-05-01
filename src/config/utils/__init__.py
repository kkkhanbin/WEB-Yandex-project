def default(value, default_value):
    """
    Получение дефолтного значения если текущее равно None

    :param value: текущее значение
    :param default_value: значение по умолчанию
    :return: аргумент value или default_value
    """

    return default_value if value is None else value


__all__ = (
    'default'
)
