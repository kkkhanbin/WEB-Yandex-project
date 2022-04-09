from collections import defaultdict

from flask import render_template, redirect
from flask_login import current_user, login_user

from src.routes import routes_bp
from src.forms import SearchForm, LoginForm
from src.data.models import User
from src.data import session


@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    form, errors = LoginForm(), defaultdict(list)

    # Если пользователь уже залогинился (такое может произойти если он сам
    # ввел адрес авторизации), перенаправляем его в профиль
    if current_user.is_authenticated:
        return redirect('/profile')

    if form.validate_on_submit():
        # Модель, у которой есть совпадения по одной из колонок
        # ['id', 'nickname', 'email'] и написанным пользователем логином
        login_model = User.find(session, form.login.data)

        # Если найдены совпадения
        if login_model is not None:
            # Если пароль верный
            if login_model.check_password(form.password.data):
                # Успешный логин пользователя
                login_user(login_model, remember=form.remember_me.data)
                return redirect('/')

        # Если логин не произошел, значит что-то пошло не так
        errors['Incorrect password'].append('Неверный пароль или логин')

    return render_template(
        'login/login.html', title='Авторизация', form=form,
        search_form=SearchForm(), errors=errors)
