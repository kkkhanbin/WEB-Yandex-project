from flask import render_template, redirect
from flask_login import current_user

from src.routes import routes_bp
from src.data.models import User
from src.data import session
from src.forms import SearchForm


@routes_bp.route('/profile/<login>')
def profile(login):
    user = User.find(session, login, abort_if_user_not_find=True)
    return render_template(
        'profile/profile.html', search_form=SearchForm(),
        title=f'Профиль пользователя {user.nickname}', user=user)


def check_user_access(login, user=None):
    """
    Проверка доступа пользователя к профилю другого пользователя

    :param login: логин другого пользователя
    :param user: проверяемый пользователь (подразумевается что будет
    использоваться текущий, поэтому он и стоит по умолчанию)
    :return: True - если пользователь имеет полный доступ к профилю или
    redirect - если что-то пошло не так
    """

    if user is None:
        user = current_user

    # Первым делом нужно проверить авторизован ли пользователь под аккаунтом,
    # который сейчас будет редактироваться
    if not user.is_authenticated:
        # Если пользователь не авторизован, пересылаем его на регистрацию
        return redirect('/register')

    if not user.check_login(login):
        # Если пользователь не является владельцем профиля, пересылаем его на
        # просмотр профиля этого человека
        return redirect(f'/profile/{login}')

    return True
