from wtforms.validators import StopValidation

from src.forms.validators.validator import Validator
from src.data import session, SqlAlchemyBase


class Unique(Validator):
    """
    Валидатор, предназначенный для проверки полей в форме или аргументов из
    парсера на уникальность в определенной таблице
    """

    # Сообщения ошибок
    DEFAULT_VALIDATION_ERROR_MESSAGE = 'Поле {column_name} уже существует'

    def __init__(self, model: SqlAlchemyBase, except_values: list=None,
                 column_name: str=None,
                 *args, **kwargs):
        """
        Инициализация валидатора уникальных значений

        :param model: модель таблицы, в которой будет осуществляться поиск
        одинаковых значений
        :param except_values: список значений, которые нужно пропускать при
        проверке. Например: идет поиск значения в колонке с почтой, в этом
        списке есть значение "example@gmail.com" и если будет найдена такая
        почта, валидатор не будет брать ее в расчет
        :param column_name: название валидируемой колонки, нужно заполнять
        только если тип валидируемого объекта - argument, так как при типе -
        field, валидатор сам находит название колонки, но если вы заполните
        его при типе - field, то оно будет приоритетнее найденного валидатором
        """

        if except_values is None:
            except_values = []

        self.column_name = column_name
        self.except_values = except_values
        self.model = model

        super().__init__(*args, **kwargs)

    def __call__(self, *args):
        super().__call__(*args)

        # Данные для валидации
        column_name = self.get_column_name(*args)
        validation_data = self.get_validation_data(*args)

        # Здесь мы ищем значение совпадения в колонке column_name, где
        # значения колонки равны переданному значению field.data и их нет в
        # except-списке
        matches = session.query(self.model).filter(
            (getattr(self.model, column_name) == validation_data) &
            (getattr(self.model, column_name).not_in(
                self.except_values))).all()

        # Если нет совпадений, то валидация прошла успешно
        if len(matches) == 0:
            return

        message = self.DEFAULT_VALIDATION_ERROR_MESSAGE.format(
            column_name=column_name) if self.message is None else self.message
        raise StopValidation(message)

    def get_column_name(self, *args):
        if self.column_name is not None:
            column_name = self.column_name
        else:
            if self.type == self.VALIDATION_FIELD_TYPE:
                column_name = args[1].name
            else:
                raise ValueError(self.COLUMN_NAME_ERROR_MESSAGE)

        return column_name
