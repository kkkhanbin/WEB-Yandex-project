from flask import Flask, Blueprint

from src.routes import routes_bp
from src.routes.handlers import handlers_bp


def register_blueprints(app: Flask, *blueprints: Blueprint) -> None:
    """
    Регистрирует blueprint`ы в приложение. Работает как
    flask.Flask.register_blueprint, но для нескольких blueprint`ов

    :param app: приложение, в которое нужно добавить blueprint`ы
    :param blueprints: сами blueprint`ы
    :return: None
    """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


BLUEPRINTS = (routes_bp, handlers_bp)

__all__ = (
    'register_blueprints', 'BLUEPRINTS'
)
