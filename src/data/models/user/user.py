from sqlalchemy import Column, Integer, String, orm
from flask_login import UserMixin
from werkzeug.security import check_password_hash

from src.data import SqlAlchemyBase
from src.data.models.model import Model


class User(Model, SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    countries = orm.relation(
        'Country', secondary='users_to_countries', backref='users',
        cascade='all, delete-orphan', single_parent=True, lazy='subquery')

    def check_password(self, password):
        return check_password_hash(self.password, password)
