from flask import redirect, render_template

from src.routes import routes_bp
from src.data.models import User, Apikey
from src.data import session
from src.forms import AddApikeyForm, SearchForm


@routes_bp.route('/profile/<login>/develop/add', methods=['GET', 'POST'])
def apikey_add(login):
    user = User.find(session, login)
    User.validate(user)

    form = AddApikeyForm()
    form.access_level.choices = user.apikey_access_levels

    if form.validate_on_submit():
        # Создание токена
        apikey = Apikey()
        apikey.load_fields(form)

        # Добавление
        session.add(apikey)
        session.commit()

        return redirect(f'/profile/{login}/develop')

    return render_template(
        'profile/develop/apikey/add/add.html', search_form=SearchForm(),
        form=form, user=user)
