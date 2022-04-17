from flask import render_template

from src.routes import routes_bp
from src.forms import SearchForm


@routes_bp.route('/')
def index():
    return render_template(
        'index.html', title='Adventure Time', search_form=SearchForm())
