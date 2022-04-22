from flask import render_template, redirect

from src.routes import routes_bp
from src.forms import SearchForm, EditWorldMapForm, get_request_field
from src.api import Static


@routes_bp.route('/', methods=['GET', 'POST'])
def index():
    form = EditWorldMapForm()

    if form.validate_on_submit():
        # Если на эту страницу перешли с формы, то пересылаем на эту же
        # страницу, но с параметром l в адресной строке. Нужно для того, чтобы
        # пользователь мог обновлять страницу без посылания новой формы
        return redirect(f'/?l={form.l.data}')

    l = get_request_field(form, 'l')
    if l is None:
        # Значение по умолчанию
        l = 'sat,skl'

    world_map = Static.create_url(params={'l': l, 'll': '0,0', 'z': 1})
    return render_template(
        'index.html', title='Adventure Time', search_form=SearchForm(),
        world_map=world_map, form=form)
