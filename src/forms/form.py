from flask_wtf import FlaskForm

from src.validators import Unique


class Form(FlaskForm):
    def add_unique_except_values(self, **except_values) -> None:
        """
        Добавляет значения, которые нужно игнорировать валидаторам Unique

        Нужно для изменения профиля, чтобы пользователь мог указать уже
        существующее, свое значение уникальной колонки и валидатор не засчитал
        это за нарушение

        :param except_values: игнорируемые значения, ключ - название колонки,
        в которую нужно добавить значения, значение - сами значения в виде
        итератора. Пример:
            nickname=['nickname1', 'nickname2']
        :return: None
        """

        for column_name, except_values in except_values.items():
            column = getattr(self, column_name)
            # Проходимся по валидаторам колонки
            for validator in column.validators:
                # Если валидатор - это валидатор уникальных значений
                if isinstance(validator, Unique):
                    # Тогда добавляем переданные нам значения
                    for value in except_values:
                        validator.except_values.append(value)
