from .config import ProductionConfig, BaseConfig, TestingConfig
from .blueprint import register_blueprints, BLUEPRINTS
from .jinja import add_tests, TESTS
import src.config.log  # Простая активация модуля
from .login import login_manager
from .rest import add_resources, RESOURCES

__all__ = (
    'ProductionConfig', 'BaseConfig', 'register_blueprints', 'add_resources',
    'add_tests', 'login_manager', 'log', 'RESOURCES', 'TestingConfig'
)
