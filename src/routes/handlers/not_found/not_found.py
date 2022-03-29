from flask import render_template
from werkzeug.exceptions import NotFound

from src.routes.handlers import handlers_bp
from src.forms import SearchForm


@handlers_bp.app_errorhandler(NotFound)
def not_found(exception):
    form = SearchForm()
    return render_template(
        'handlers/not_found/not_found.html', search_form=form)
