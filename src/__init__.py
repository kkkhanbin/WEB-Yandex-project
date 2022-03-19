import logging

from flask import Flask

from src.config import Config

# Создание приложения
app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(level=logging.INFO)
