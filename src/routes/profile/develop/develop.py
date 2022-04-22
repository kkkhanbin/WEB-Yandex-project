from flask import render_template
from werkzeug.exceptions import Forbidden

from src.routes import routes_bp
from src.data.models import User, Apikey
from src.data import session
from src.forms import SearchForm
from src.data.models.validators import ModelNotFound, UserUnauthorized, \
    UserToUser


@routes_bp.route('/profile/<login>/develop')
def develop(login):
    user, forbidden = User.find(session, login), False
    try:
        User.validate(
            UserUnauthorized(), ModelNotFound(user), UserToUser(user))
    except Forbidden:
        forbidden = True
    apikeys = Apikey.find_fields(session, Apikey, owner=user.id)

    return render_template(
        'profile/develop/develop.html', search_form=SearchForm(),
        title=f'Кабинет разработчика пользователя {user.nickname}', user=user,
        apikeys=apikeys, forbidden=forbidden)
