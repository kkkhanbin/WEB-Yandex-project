from flask import render_template
from werkzeug.exceptions import NotFound

from src.routes import routes_bp
from src.data.models import User, Apikey
from src.data import session
from src.forms import SearchForm


@routes_bp.route('/profile/<login>/develop')
def develop(login):
    user = User.find(session, login)
    User.validate(user, validators=[NotFound])
    apikeys = Apikey.find_fields(session, Apikey, owner=user.id)

    return render_template(
        'profile/develop/develop.html', search_form=SearchForm(),
        title=f'Кабинет разработчика пользователя {user.nickname}', user=user,
        apikeys=apikeys)
