from flask import render_template

from src.routes import routes_bp
from src.data import find_user
from src.forms import SearchForm


@routes_bp.route('/profile/<login>')
def profile(login):
    user = find_user(login)

    return render_template(
        'profile/profile.html', search_form=SearchForm(),
        title=f'Профиль пользователя {user.nickname}', user=user)
