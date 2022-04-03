import logging

from dotenv import load_dotenv
load_dotenv('.env')

from flask import Flask
from flask_restful import Api

from src.routes import routes_bp
from src.routes.handlers import handlers_bp
from src.config import ProductionConfig, register_blueprints
from src.config.jinja import TESTS, add_tests
from src.config.rest import add_resources
from src.config.login import login_manager

# Создание приложения и его конфигурация
app = Flask(__name__)
app.config.from_object(ProductionConfig)

# Регистрация REST Api
api = Api(app)

resources = ()
add_resources(api, *resources)

# Конфигурация jinja
add_tests(app.jinja_env, TESTS)

# Регистрация Blueprint`ов
blueprints = (routes_bp, handlers_bp)
register_blueprints(app, *blueprints)

# login manager
login_manager.init_app(app)

# Конфигурация модуля logging
logging.basicConfig(level=logging.INFO)
