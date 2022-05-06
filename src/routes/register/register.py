from flask import redirect, render_template
from flask_login import current_user

from src.forms import RegisterForm, SearchForm
from src.routes import routes_bp
from src.data.models import User
from src.data import session

TITLE = 'Регистрация'


@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Если пользователь уже залогинился (такое может произойти если он сам
    # ввел адрес регистрации), перенаправляем его в профиль
    if current_user.is_authenticated:
        return redirect(f'/profile/{current_user.nickname}')

    form = RegisterForm()

    # Процесс добавления пользователя
    if form.validate_on_submit():
        User.register(session, form)
        return redirect('/')

    return render_template(
        'register/register.html', title=TITLE, form=form,
        search_form=SearchForm())
