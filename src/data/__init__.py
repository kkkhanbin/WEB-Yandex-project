import os

from src.data.db_session import create_session, global_init, SqlAlchemyBase

global_init(os.environ.get('DB_PATH', 'db/database.db'))
session = create_session()


def find_fields(model: SqlAlchemyBase, columns: list, value) -> list or None:
    """
    Поиск поля в таблице по нескольким колонкам

    :param model: модель, в таблице которой, нужно искать
    :param columns: названия колонок, по которым нужно искать.
    Их порядок важен, так как функция возвращает первые попавшиеся значения
    :param value: искомое значение
    :return: список моделей, в случае нахождения или None
    """

    for column in columns:
        fields = session.query(model).filter(
            getattr(model, column) == value).all()
        if len(fields) > 0:
            return fields


__all__ = (
    'create_session', 'global_init', 'SqlAlchemyBase', 'session'
)
