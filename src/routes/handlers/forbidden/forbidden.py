from flask import render_template
from werkzeug.exceptions import Forbidden

from src.routes.handlers import handlers_bp
from src.forms import SearchForm


@handlers_bp.app_errorhandler(Forbidden)
def forbidden(error):
    return render_template(
        'handlers/forbidden/forbidden.html', search_form=SearchForm(),
        error=error)
