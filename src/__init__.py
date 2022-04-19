from dotenv import load_dotenv
load_dotenv('.env')

from flask import Flask
from flask_restful import Api

from src.config import ProductionConfig, register_blueprints, RESOURCES, \
    add_resources, add_tests, TESTS, BLUEPRINTS, login_manager
from src.data.resources import UserResource

# Создание приложения и его конфигурация
app = Flask(__name__)
app.config.from_object(ProductionConfig)

# Регистрация REST Api
api = Api(app)
add_resources(api, *RESOURCES)

# Конфигурация jinja
add_tests(app.jinja_env, TESTS)

# Регистрация Blueprint`ов
register_blueprints(app, *BLUEPRINTS)

# login manager
login_manager.init_app(app)
