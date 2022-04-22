import os


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JSON_AS_ASCII = False
    TRAP_HTTP_EXCEPTIONS = True
    UPLOAD_FOLDER = os.path.join('static', 'upload')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 мегабайт


class ProductionConfig(BaseConfig):
    DEBUG = False


class TestingConfig(BaseConfig):
    DEBUG = True


__all__ = (
    'BaseConfig', 'ProductionConfig', 'TestingConfig'
)
