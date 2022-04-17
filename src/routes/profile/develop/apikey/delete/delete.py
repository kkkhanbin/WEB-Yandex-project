from flask import redirect

from src.routes import routes_bp
from src.data.models import User, Apikey
from src.data import session


@routes_bp.route('/profile/<login>/develop/<int:apikey_id>/delete')
def apikey_delete(login, apikey_id):
    user = User.find(session, login)
    apikey = session.query(Apikey).get(apikey_id)

    # Валидация токена
    Apikey.validate(apikey, user=user)

    session.delete(apikey)
    session.commit()

    return redirect(f'/profile/{user.nickname}/develop')
