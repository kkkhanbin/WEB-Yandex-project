import os

from flask import render_template, abort, redirect
from werkzeug.exceptions import NotFound

from src.routes import routes_bp
from src.data.models import Place
from src.data import session
from src.forms import SearchForm, AddPlaceMediaForm

TITLE = 'Посещенное место "{place_name}" пользователя {user_nickname}'


@routes_bp.route(
    '/places/<login>/<int:place_id>',
    defaults={'path': '/'},
    methods=['GET', 'POST'])
@routes_bp.route(
    '/places/<login>/<int:place_id>/<path:path>',
    methods=['GET', 'POST'])
def place(login, place_id, path):
    user, place, file_path, media_path, path = \
        Place.get_view_config(session, login, place_id, path)

    try:
        listdir = os.listdir(file_path)
    except FileNotFoundError:
        abort(NotFound.code, description=Place.FILE_NOT_FOUND_MESSAGE)
    except NotADirectoryError:
        listdir = None

    form = AddPlaceMediaForm()
    if form.validate_on_submit():
        place.save_place_media(form.files.data + form.folders.data, user.id)
        return redirect(f'/places/{user.nickname}/{place.id}')

    return render_template(
        'places/place/place.html',
        search_form=SearchForm(),
        title=TITLE.format(place_name=place.name, user_nickname=user.nickname),
        user=user,
        place=place,
        file_path=file_path,
        path=path,
        listdir=listdir,
        form=form,
        media_path=media_path
    )
