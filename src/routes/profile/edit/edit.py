from flask import render_template, redirect

from ..profile import check_user_access
from src.routes import routes_bp
from src.data import session
from src.data.models import User
from src.forms import SearchForm, AddEditProfileForm


@routes_bp.route('/profile/<login>/edit', methods=['GET', 'POST'])
def edit(login):
    response = check_user_access(login)
    if response is not True:
        return response

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
