from flask import redirect

from src.routes import routes_bp
from src.data.models import Place
from src.data import session


@routes_bp.route('/places/<login>/<int:place_id>/delete')
def place_delete(login, place_id):
    user, place = Place.get_view_config(session, login, place_id)

    session.delete(place)
    session.commit()

    return redirect(f'/places/{user.nickname}')
