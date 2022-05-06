import os

from flask import redirect

from src.routes import routes_bp
from src.data.models import Place
from src.data import session
from src.config.constants import PLACE_PATH


@routes_bp.route('/places/<login>/<int:place_id>/delete')
def place_delete(login, place_id):
    user, place = Place.get_view_config(session, login, place_id)

    Place.delete(session, place)
    Place.delete_file(
        os.path.join(*PLACE_PATH).format(
            profile_id=user.id, place_id=place.id))

    return redirect(f'/places/{user.nickname}')
