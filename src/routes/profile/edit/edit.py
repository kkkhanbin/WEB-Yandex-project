from flask_login import current_user
from flask import render_template, redirect

from src.routes import routes_bp
from src.data import session
from src.data.models import User
from src.forms import SearchForm, AddEditProfileForm


@routes_bp.route('/profile/<login>/edit', methods=['GET', 'POST'])
def edit(login):
    # Первым делом нужно проверить авторизован ли пользователь под аккаунтом,
    # который сейчас будет редактироваться
    if not current_user.is_authenticated:
        # Если пользователь не авторизован, пересылаем его на регистрацию
        return redirect('/register')
    if not current_user.check_login(login):
        # Если пользователь не является владельцем профиля, пересылаем его на
        # просмотр профиля этого человека
        return redirect(f'/profile/{login}')

    user = User.find(session, login)
    form = AddEditProfileForm()
    form.add_unique_except_values(
        {'column_name': 'nickname', 'except_values': [user.nickname]},
        {'column_name': 'email', 'except_values': [user.email]}
    )

    if form.validate_on_submit():
        user.load_fields(form)
        session.commit()

        # Сохранение фото профиля
        user.save_avatar_image(form.avatar_image.data)

        return redirect('/')

    return render_template(
        'profile/edit/edit.html', search_form=SearchForm(),
        title=f'Редактирование профиля пользователя {user.nickname}',
        user=user, form=form)
