import os

from src.data.db_session import create_session, global_init, SqlAlchemyBase
from src.data.models import User

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


def find_user(login) -> User or None:
    """
    Поиск пользователя по нескольким колонкам

    Является упрощением функции find_fields для поиска пользователя. Благодаря
    этой функции, можно менять порядок колонок для поиска пользователя

    :param login: искомое значение колонки
    :return: User, если пользователь найден, иначе - None
    """
    response = find_fields(User, ['id', 'nickname', 'email'], login)
    if response is not None:
        return response[0]
    return response


__all__ = (
    'create_session', 'global_init', 'SqlAlchemyBase', 'session'
)
