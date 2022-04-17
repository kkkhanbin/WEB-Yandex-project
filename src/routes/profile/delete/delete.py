from flask import render_template, redirect

from src.routes import routes_bp
from src.data.models import User
from src.data import session
from src.forms import SearchForm, DeleteProfileForm


@routes_bp.route('/profile/<login>/delete', methods=['GET', 'POST'])
def delete(login):
    user = User.find(session, login)
    User.validate(user)

    form = DeleteProfileForm()
    if form.validate_on_submit():
        session.delete(user)
        session.commit()
        return redirect('/logout')

    return render_template(
        'profile/delete/delete.html',
        search_form=SearchForm(),
        title=f'Удаление профиля пользователя {user.nickname}',
        user=user,
        form=form
    )
