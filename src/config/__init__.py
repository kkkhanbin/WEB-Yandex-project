import src.config.log  # Простая активация модуля
from .configs import ProductionConfig, BaseConfig, TestingConfig, config
from .blueprint import register_blueprints, BLUEPRINTS
from .jinja import add_tests, TESTS
from .login import login_manager
from .rest import add_resources, RESOURCES
from .constants import PLACE_PATH, PROFILE_PATH, PLACES_PATH, PROFILES_PATH, \
    PLACE_MEDIA_FILES_PATH, STATIC_PATH, AVATAR_PATH, UPLOAD_PATH
from .utils import default

__all__ = (
    'ProductionConfig', 'BaseConfig', 'register_blueprints', 'add_resources',
    'add_tests', 'login_manager', 'log', 'RESOURCES', 'TestingConfig',
    'PLACE_MEDIA_FILES_PATH', 'PLACE_PATH', 'PLACES_PATH', 'PROFILES_PATH',
    'PROFILE_PATH', 'AVATAR_PATH', 'STATIC_PATH', 'BLUEPRINTS', 'UPLOAD_PATH',
    'config'
)
