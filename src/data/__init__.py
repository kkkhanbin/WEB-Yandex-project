from src.config import config
from src.data.db_session import create_session, global_init, SqlAlchemyBase

global_init(config.DB_PATH)
session = create_session()

__all__ = (
    'create_session', 'global_init', 'SqlAlchemyBase', 'session'
)
