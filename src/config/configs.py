import os


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    JSON_AS_ASCII = False
    TRAP_HTTP_EXCEPTIONS = True
    UPLOAD_FOLDER = os.path.join('static', 'upload')
    MAX_CONTENT_SIZE = 16 * 1024 * 1024  # 16 мегабайт
    MAX_PLACE_MEDIA_SIZE = 16 * 1024 * 1024  # 16 мегабайт
    ALLOWED_EXTENSIONS = (
        'png', 'jpg', 'svg', 'mp3', 'mp4', 'mpeg-1', 'mpeg-2', 'mpeg-3',
        'mpeg-4', 'txt', 'csv', 'db', 'py', 'js', 'html'
    )
    FORBIDDEN_EXTENSIONS = (
        'exe'
    )
    DB_PATH = os.path.join('db', 'database.db')


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    DEBUG = True
    BUNDLE_ERRORS = True


# Здесь можно настраивать текущий конфиг
config = ProductionConfig

__all__ = (
    'BaseConfig', 'ProductionConfig', 'TestingConfig', 'config'
)
