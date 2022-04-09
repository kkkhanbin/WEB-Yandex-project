from flask_wtf import FlaskForm

from src.forms.validators import Unique


class Form(FlaskForm):
    def add_unique_except_values(self, *except_values: dict) -> None:
        """
        Добавляет значения, которые нужно игнорировать валидаторам Unique

        Нужно для изменения профиля, чтобы пользователь мог указать уже
        существующее, свое значение уникальной колонки и валидатор не засчитал
        это за нарушение

        :param except_values: словарь, в котором должны быть ключи:
        column_name - название колонки, в которую нужно добавить значения и
        except_values - сами значения в виде итератора. Пример:
        {
            'column_name': 'nickname',
            'except_values': ['nickname1', 'nickname2']
        }
        :return: None
        """

        for except_value in except_values:
            column = getattr(self, except_value['column_name'])
            # Проходимся по валидаторам колонки
            for validator in column.validators:
                # Если валидатор - это валидатор уникальных значений
                if isinstance(validator, Unique):
                    # Тогда добавляем переданные нам значения
                    for value in except_value['except_values']:
                        validator.except_values.append(value)
