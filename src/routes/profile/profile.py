from flask import render_template
from werkzeug.exceptions import NotFound

from src.routes import routes_bp
from src.data.models import User
from src.data import session
from src.forms import SearchForm


@routes_bp.route('/profile/<login>')
def profile(login):
    user = User.find(session, login)
    User.validate(user, validators=[NotFound])
    return render_template(
        'profile/profile.html', search_form=SearchForm(),
        title=f'Профиль пользователя {user.nickname}', user=user)
