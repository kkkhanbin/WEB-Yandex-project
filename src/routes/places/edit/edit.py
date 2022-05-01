from flask import redirect, render_template

from src.routes import routes_bp
from src.data.models import Place
from src.data import session
from src.forms import AddPlaceForm, SearchForm


@routes_bp.route('/places/<login>/<int:place_id>/edit',
                 methods=['GET', 'POST'])
def place_edit(login, place_id):
    user, place = Place.get_view_config(session, login, place_id)

    form = AddPlaceForm()
    if form.validate_on_submit():
        # Загрузка изменений
        place.load_fields(user, form)

        # Сохранение изменений
        session.commit()

        return redirect(f'/places/{login}')

    return render_template(
        'places/edit/edit.html', search_form=SearchForm(),
        form=form, place=place, user=user)
