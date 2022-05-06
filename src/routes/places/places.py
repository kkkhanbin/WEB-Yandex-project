from flask import render_template
from werkzeug.exceptions import Forbidden

from src.routes import routes_bp
from src.data.models import Place, User
from src.data import session
from src.forms import SearchForm
from src.data.models.validators import ModelNotFound, UserToUser, \
    UserUnauthorized

TITLE = 'Посещенные места пользователя {user_nickname}'


@routes_bp.route('/places/<login>')
def places(login):
    user = User.find(session, login)
    try:
        User.validate(
            UserUnauthorized(user), ModelNotFound(user), UserToUser(user))
    except Forbidden:
        forbidden = True
    else:
        forbidden = False

    places = Place.find_fields(session, owner=user.id)

    return render_template(
        'places/places.html', search_form=SearchForm(),
        title=TITLE.format(user_nickname=user.nickname), user=user,
        places=places, forbidden=forbidden)
