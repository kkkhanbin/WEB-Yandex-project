from flask import request, render_template, redirect
from flask_wtf import FlaskForm

from src.forms import SearchForm
from src.routes import routes_bp
from src.routes.results.search import Search


def get_request_text(form: FlaskForm=None) -> str or None:
    """
    Получение текста запроса

    Поиск проходит по переданной форме или в аргументах адресной строки

    :param form: форма, обладающая полем text, из которого будет взят текст
    :return: найденный текст или None
    """
    if 'text' in request.args:
        # Обработка запроса через аргументы адресной строки
        return request.args['text']

    if form is not None and form.validate_on_submit():
        # Обработка запроса через форму поиска
        return form.text.data


@routes_bp.route('/results', methods=['GET', 'POST'])
def results():
    form = SearchForm()
    request_text = get_request_text(form)

    if form.validate_on_submit():
        # Если пользователь пришел с формы, т.е. с POST запроса, пересылаем его
        # на этот же обработчик, но через GET запрос и поисковый текст передаем
        # в аргументах адресной строки.
        return redirect(f'/results?text={request_text}')

    return render_template(
        'results/results.html',
        title=f'Результат поиска по запросу {request_text}', search_form=form,
        results=Search.search(request_text))
