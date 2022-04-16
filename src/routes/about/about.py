from flask import render_template

from src.forms import SearchForm
from src.routes import routes_bp


@routes_bp.route('/about')
def about():
    return render_template(
        'about/about.html', title=f'Информация о сайте',
        search_form=SearchForm())
