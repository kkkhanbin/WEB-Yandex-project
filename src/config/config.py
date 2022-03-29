import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JSON_AS_ASCII = False
    TRAP_HTTP_EXCEPTIONS = True
    UPLOAD_FOLDER = os.path.join('static', 'upload')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'svg'}
