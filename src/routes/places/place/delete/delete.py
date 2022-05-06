import os

from flask import abort, redirect
from werkzeug.exceptions import NotFound, Forbidden

from src.routes import routes_bp
from src.data.models import Place
from src.data import session

DELETE_ROOT_FOLDER_MESSAGE = 'Вы не можете удалить корневую папку'


@routes_bp.route(
    '/places/<login>/delete/<int:place_id>', defaults={'path': '/'})
@routes_bp.route('/places/<login>/delete/<int:place_id>/<path:path>')
def place_media_delete(login, place_id, path):
    user, place, file_path, media_path, path = \
        Place.get_view_config(session, login, place_id, path)

    try:
        # Чтобы нельзя было удалять корневую папку медиа файлов
        if len(path) == 0:
            abort(Forbidden.code,
                  description=DELETE_ROOT_FOLDER_MESSAGE)

        path_split = os.path.split(path)
        back_path = os.path.join(*path_split[:-1])
        if back_path:
            back_path = '/' + back_path

        place.delete_file(file_path)

    except FileNotFoundError:
        abort(NotFound.code, description=Place.FILE_NOT_FOUND_MESSAGE)

    return redirect(f'/places/{user.nickname}/{place.id}{back_path}')
