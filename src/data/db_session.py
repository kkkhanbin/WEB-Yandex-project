import logging

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception('Необходимо указать файл базы данных.')

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sa.create_engine(conn_str, echo=False, encoding='utf8')
    __factory = orm.sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)

    logging.info(f'Было подключено соединение по адресу {conn_str}')


def create_session() -> Session:
    global __factory
    return __factory()
