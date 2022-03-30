from collections import defaultdict

from flask import render_template, redirect
from flask_login import current_user, login_user

from src.routes import routes_bp
from src.forms import SearchForm, LoginForm
from src.data import find_fields
from src.data.models import User


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
        login_model = find_fields(
            User, ['id', 'nickname', 'email'], form.login.data)

        # Если найдены совпадения
        if login_model is not None:
            # Так как функция find_fields возвращает список, мы берем первое
            # значение потому что проверка шла на уникальные поля и
            # несколько совпадений быть не может
            login_model = login_model[0]

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
