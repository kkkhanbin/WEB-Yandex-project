from flask import Flask, Blueprint

from .config import ProductionConfig, BaseConfig


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


__all__ = (
    'ProductionConfig', 'BaseConfig'
)
