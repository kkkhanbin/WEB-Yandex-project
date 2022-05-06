from flask import redirect

from src.routes import routes_bp
from src.data.models import User, Apikey
from src.data import session
from src.data.models.validators import ModelNotFound, UserUnauthorized, \
    UserToUser, OwnerToModel


@routes_bp.route('/profile/<login>/develop/<int:apikey_id>/delete')
def apikey_delete(login, apikey_id):
    # Пользователь
    user = User.find(session, login)
    User.validate(UserUnauthorized(), ModelNotFound(user), UserToUser(user))

    # Токен
    apikey = session.query(Apikey).get(apikey_id)
    Apikey.validate(ModelNotFound(apikey), OwnerToModel(apikey, user=user))

    Apikey.delete(session, apikey)

    return redirect(f'/profile/{user.nickname}/develop')
