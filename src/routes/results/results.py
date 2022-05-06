from flask import render_template, redirect
from werkzeug.exceptions import BadRequest

from src.forms import SearchForm
from src.routes import routes_bp
from src.search import Search
from src.parsers import SearchParser

TITLE = 'Результат поиска по запросу {text}'


@routes_bp.route('/results', methods=['GET', 'POST'])
def results():
    form = SearchForm()

    try:
        args = SearchParser().parse_args()
    except BadRequest:
        request_text = ''
    else:
        request_text = args.text

    if form.validate_on_submit():
        # Если пользователь пришел с формы, т.е. с POST запроса, пересылаем его
        # на этот же обработчик, но через GET запрос и поисковый текст передаем
        # в аргументах адресной строки.
        return redirect(f'/results?text={request_text}')

    search_results = Search.search(request_text)
    return render_template(
        'results/results.html',
        title=TITLE.format(text=request_text),
        search_form=form,
        results=search_results)
