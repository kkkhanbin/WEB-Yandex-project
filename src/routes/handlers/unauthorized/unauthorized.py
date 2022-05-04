import logging

from flask import render_template
from werkzeug.exceptions import Unauthorized

from src.routes.handlers import handlers_bp
from src.forms import SearchForm


@handlers_bp.app_errorhandler(Unauthorized)
def unauthorized(error):
    logging.error(f'Ошибка не авторизованного пользователя - {error}')
    return render_template(
        'handlers/unauthorized/unauthorized.html', search_form=SearchForm(),
        error=error)
