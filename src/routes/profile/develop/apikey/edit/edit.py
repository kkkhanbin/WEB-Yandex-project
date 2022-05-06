from flask import redirect, render_template
from flask_login import current_user

from src.routes import routes_bp
from src.data.models import User, Apikey
from src.data import session
from src.forms import AddApikeyForm, SearchForm
from src.data.models.validators import ModelNotFound, UserUnauthorized, \
    UserToUser, Blocked, OwnerToModel

TITLE = 'Редактирование API-ключа {apikey_name}'


@routes_bp.route('/profile/<login>/develop/<int:apikey_id>/edit',
                 methods=['GET', 'POST'])
def apikey_edit(login, apikey_id):
    # Пользователь
    user = User.find(session, login)
    User.validate(UserUnauthorized(), ModelNotFound(user), UserToUser(user))

    # Токен
    apikey = Apikey.find(session, apikey_id)
    Apikey.validate(
        ModelNotFound(apikey), OwnerToModel(apikey, user=user),
        Blocked(apikey, Apikey.BLOCKED_MESSAGE))

    # Форма
    form = AddApikeyForm()
    form.access_level.choices = current_user.apikey_access_levels

    if form.validate_on_submit():
        Apikey.edit(session, form, apikey)
        return redirect(f'/profile/{login}/develop')

    return render_template(
        'profile/develop/apikey/edit/edit.html', search_form=SearchForm(),
        form=form, apikey=apikey, user=user,
        title=TITLE.format(apikey_name=apikey.name))
