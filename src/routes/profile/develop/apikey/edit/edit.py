from flask import redirect, render_template
from flask_login import current_user

from src.routes import routes_bp
from src.data.models import User, Apikey
from src.data import session
from src.forms import AddApikeyForm, SearchForm


@routes_bp.route('/profile/<login>/develop/<int:apikey_id>/edit',
                 methods=['GET', 'POST'])
def apikey_edit(login, apikey_id):
    # Нахождение пользователя
    user, forbidden = User.find(session, login), False
    User.validate(user)

    # Нахождение токена
    apikey = Apikey.find_fields(session, Apikey, id=apikey_id)
    Apikey.validate(apikey)
    apikey = apikey[0]

    # Форма
    form = AddApikeyForm()
    form.access_level.choices = current_user.apikey_access_levels

    if form.validate_on_submit():
        # Загрузка изменений
        apikey.load_fields(form)

        # Сохранение изменений
        session.commit()

        return redirect(f'/profile/{login}/develop')

    return render_template(
        'profile/develop/apikey/edit/edit.html', search_form=SearchForm(),
        form=form, apikey=apikey, user=user)
