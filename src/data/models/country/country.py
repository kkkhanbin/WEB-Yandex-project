from sqlalchemy import Column, Integer, String, Table, ForeignKey

from src.data import SqlAlchemyBase
from src.data.models.model import Model

users_to_countries = Table(
    'users_to_countries', SqlAlchemyBase.metadata,
    Column('users', Integer, ForeignKey('users.id')),
    Column('countries', Integer, ForeignKey('countries.id')),
    extend_existing=True
)


class Country(Model, SqlAlchemyBase):
    __tablename__ = 'countries'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=True)
