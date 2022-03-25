import os
import logging

from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from src.config import Config
from src.routes import routes_bp
from src.data import global_init


def add_resources(api: Api, *resources) -> None:
    """
    Добавляет ресурсы в Api

    Args:
        api: Экземпляр класса flask_restful.Api, которому будут добавляться
            ресурсы
        resources: Коллекция, где первое значение - добавляемый ресурс,
            а второе - его url
    Returns:
        None
    """

    for resource, route in resources:
        api.add_resource(resource, route)


# Создание приложения
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация БД
global_init(os.environ.get('DB_PATH'))

# Регистрация REST Api
api = Api(app)

resources = ()
add_resources(api, *resources)

# Регистрация Blueprint`ов
app.register_blueprint(routes_bp)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Конфигурация модуля logging
logging.basicConfig(level=logging.INFO)
