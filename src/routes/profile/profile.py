from flask import render_template

from src.routes import routes_bp
from src.data.models import User
from src.data import session
from src.forms import SearchForm
from src.data.models.validators import ModelNotFound

TITLE = 'Профиль пользователя {user_nickname}'


@routes_bp.route('/profile/<login>')
def profile(login):
    user = User.find(session, login)
    User.validate(ModelNotFound(user))

    return render_template(
        'profile/profile.html', search_form=SearchForm(),
        title=TITLE.format(user_nickname=user.nickname), user=user)
