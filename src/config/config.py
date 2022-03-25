import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JSON_AS_ASCII = False
