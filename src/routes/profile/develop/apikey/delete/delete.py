from flask import redirect

from src.routes import routes_bp
from src.data.models import User, Apikey
from src.data import session
from src.data.models.validators import ModelNotFound, UserUnauthorized, \
    UserToUser, UserToApikey


@routes_bp.route('/profile/<login>/develop/<int:apikey_id>/delete')
def apikey_delete(login, apikey_id):
    # Пользователь
    user = User.find(session, login)
    User.validate(UserUnauthorized(), ModelNotFound(user), UserToUser(user))

    # Токен
    apikey = session.query(Apikey).get(apikey_id)
    Apikey.validate(ModelNotFound(apikey), UserToApikey(user, apikey))

    session.delete(apikey)
    session.commit()

    return redirect(f'/profile/{user.nickname}/develop')
