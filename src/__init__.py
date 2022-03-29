import logging

from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from src.data.models import User
from src.data import create_session, global_init
from src.config import Config
from src.routes import routes_bp
from src.routes.handlers import handlers_bp


def add_resources(api: Api, *resources) -> None:
    """
    Добавляет ресурсы в Api

    :param api: Экземпляр класса flask_restful.Api, которому будут добавляться
            ресурсы
    :param resources: Коллекция, где первое значение - добавляемый ресурс,
            а второе - его url
    :return: None
    """

    for resource, route in resources:
        api.add_resource(resource, route)


# Создание приложения
app = Flask(__name__)
app.config.from_object(Config)

# Регистрация REST Api
api = Api(app)

resources = ()
add_resources(api, *resources)

# Регистрация Blueprint`ов
app.register_blueprint(routes_bp)
app.register_blueprint(handlers_bp)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


# Конфигурация модуля logging
logging.basicConfig(level=logging.INFO)
