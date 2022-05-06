from flask import render_template

from src.forms import SearchForm
from src.routes import routes_bp

TITLE = 'Информация о сайте'


@routes_bp.route('/about')
def about():
    return render_template(
        'about/about.html', title=TITLE,
        search_form=SearchForm())
