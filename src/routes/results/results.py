from flask import render_template, redirect

from src.forms import SearchForm, get_request_field
from src.routes import routes_bp
from src.routes.results.search import Search


@routes_bp.route('/results', methods=['GET', 'POST'])
def results():
    form = SearchForm()
    request_text = get_request_field(form, 'text')

    if form.validate_on_submit():
        # Если пользователь пришел с формы, т.е. с POST запроса, пересылаем его
        # на этот же обработчик, но через GET запрос и поисковый текст передаем
        # в аргументах адресной строки.
        return redirect(f'/results?text={request_text}')

    return render_template(
        'results/results.html',
        title=f'Результат поиска по запросу {request_text}', search_form=form,
        results=Search.search(request_text))
