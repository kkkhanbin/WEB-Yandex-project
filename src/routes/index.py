from flask import render_template, redirect
from werkzeug.exceptions import BadRequest

from src.parsers import MapParser
from src.routes import routes_bp
from src.forms import SearchForm, EditMapForm
from src.api import Static

DEFAULT_MAP_PARAMS = {'l': 'map', 'll': '0,0', 'z': '1'}


@routes_bp.route('/', methods=['GET', 'POST'])
def index():
    form = EditMapForm()

    if form.validate_on_submit():
        # Если на эту страницу перешли с формы, то пересылаем на эту же
        # страницу, но с параметром l в адресной строке. Нужно для того, чтобы
        # пользователь мог обновлять страницу без посылания новой формы
        l = form.L_TYPES_CONVERT[form.l.data]
        lon, lat = form.longitude.data, form.latitude.data
        z = form.z.data

        return redirect(
            Static.create_url(
                '/', params={'l': l, 'lon': lon, 'lat': lat, 'z': z})
        )

    try:
        map_args = MapParser().parse_args()
    except BadRequest:
        map_params = DEFAULT_MAP_PARAMS
    else:
        map_params = {
            'l': map_args.l,
            'll': f'{map_args.lon},{map_args.lat}',
            'z': map_args.z
        }

    world_map = Static.get(params=map_params)
    if not world_map:
        world_map = Static.get(params=DEFAULT_MAP_PARAMS)

    return render_template(
        'index.html', title='Adventure Time', search_form=SearchForm(),
        world_map=world_map.url, form=form, map_params=map_params)
