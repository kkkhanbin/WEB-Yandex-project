import os

from src.data.db_session import create_session, global_init, SqlAlchemyBase

global_init(os.environ.get('DB_PATH', 'db/database.db'))
session = create_session()

__all__ = (
    'create_session', 'global_init', 'SqlAlchemyBase', 'session'
)
