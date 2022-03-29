from flask import render_template, redirect

from src.routes import routes_bp
from src.forms import SearchForm


@routes_bp.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(f'/results/?text={form.text.data}')

    return render_template(
        'index.html', title='Adventure Time', search_form=form)
