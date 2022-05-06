import os

from flask import redirect, render_template

from src.routes import routes_bp
from src.data.models import User, Place
from src.data import session
from src.forms import AddPlaceForm, SearchForm
from src.data.models.validators import ModelNotFound, UserUnauthorized, \
    UserToUser
from src.config.constants import PLACE_MEDIA_FILES_PATH

TITLE = 'Добавление посещенного места'


@routes_bp.route('/places/<login>/add', methods=['GET', 'POST'])
def place_add(login):
    user = User.find(session, login)
    User.validate(UserUnauthorized(), ModelNotFound(user), UserToUser(user))

    form = AddPlaceForm()
    if form.validate_on_submit():
        # Создание токена
        place = Place.add(session, form)

        # Создание директории для файлов посещенного места
        place.create_dir(os.path.join(*PLACE_MEDIA_FILES_PATH).format(
            profile_id=user.id, place_id=place.id))

        return redirect(f'/places/{login}')

    return render_template(
        'places/add/add.html', search_form=SearchForm(), form=form, user=user,
        title=TITLE)
