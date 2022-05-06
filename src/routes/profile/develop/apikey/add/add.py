from flask import redirect, render_template

from src.routes import routes_bp
from src.data.models import User, Apikey
from src.data import session
from src.forms import AddApikeyForm, SearchForm
from src.data.models.validators import ModelNotFound, UserUnauthorized, \
    UserToUser

TITLE = 'Добавление нового API-ключа'


@routes_bp.route('/profile/<login>/develop/add', methods=['GET', 'POST'])
def apikey_add(login):
    user = User.find(session, login)
    User.validate(UserUnauthorized(), ModelNotFound(user), UserToUser(user))

    form = AddApikeyForm()
    form.access_level.choices = user.apikey_access_levels

    if form.validate_on_submit():
        Apikey.add(session, form)
        return redirect(f'/profile/{login}/develop')

    return render_template(
        'profile/develop/apikey/add/add.html', search_form=SearchForm(),
        form=form, user=user, title=TITLE)
