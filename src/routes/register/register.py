from flask import redirect, render_template
from flask_login import current_user, login_user

from src.forms import AddEditProfileForm, SearchForm
from src.routes import routes_bp
from src.data.models import User
from src.data import session


@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Если пользователь уже залогинился (такое может произойти если он сам
    # ввел адрес регистрации), перенаправляем его в профиль
    if current_user.is_authenticated:
        return redirect('/profile')

    form = AddEditProfileForm()

    # Процесс добавления пользователя
    if form.validate_on_submit():
        user = User()
        user.load_fields(form)

        session.add(user)
        session.commit()

        # Сохранение фото профиля
        user.save_avatar_image(form.avatar_image.data)

        # Если включена галочка на вход после регистрации
        if form.login.data:
            login_user(user, remember=True)

        return redirect('/')

    return render_template(
        'register/register.html', title='Регистрация', form=form,
        search_form=SearchForm())
