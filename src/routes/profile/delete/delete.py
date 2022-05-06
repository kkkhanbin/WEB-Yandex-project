from flask import render_template, redirect

from src.routes import routes_bp
from src.data.models import User, Apikey, Place
from src.data import session
from src.forms import SearchForm, DeleteProfileForm
from src.data.models.validators import ModelNotFound, UserUnauthorized, \
    UserToUser

TITLE = 'Удаление профиля пользователя {user_nickname}'


@routes_bp.route('/profile/<login>/delete', methods=['GET', 'POST'])
def delete(login):
    user = User.find(session, login)
    User.validate(UserUnauthorized(), ModelNotFound(user), UserToUser(user))

    form = DeleteProfileForm()
    if form.validate_on_submit():
        # Удаление всех мест и API-ключей
        session.query(Place).filter(Place.owner == user.id).delete()
        session.query(Apikey).filter(Apikey.owner == user.id).delete()
        session.commit()

        # Удаление всех директорий пользователя и самого пользователя
        user.delete_profile_dirs()
        User.delete(session, user)

        return redirect('/logout')

    return render_template(
        'profile/delete/delete.html',
        search_form=SearchForm(),
        title=TITLE.format(user_nickname=user.nickname),
        user=user,
        form=form
    )
