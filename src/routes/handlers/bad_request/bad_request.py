import logging

from flask import render_template
from werkzeug.exceptions import BadRequest

from src.routes.handlers import handlers_bp
from src.forms import SearchForm


@handlers_bp.app_errorhandler(BadRequest)
def bad_request(error):
    logging.error(f'Неккоректный запрос - {error}')
    return render_template(
        'handlers/bad_request/bad_request.html', search_form=SearchForm(),
        error=error)
