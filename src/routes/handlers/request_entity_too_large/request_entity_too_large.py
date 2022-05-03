from werkzeug.exceptions import RequestEntityTooLarge
from flask import render_template

from src.routes.handlers import handlers_bp
from src.forms import SearchForm


@handlers_bp.app_errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    form = SearchForm()
    return render_template(
        'handlers/request_entity_too_large/request_entity_too_large.html',
        search_form=form, error=error)
