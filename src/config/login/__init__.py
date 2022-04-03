from flask_login import LoginManager

from src.data.models import User
from src.data import create_session

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


__all__ = (
    'login_manager', 'load_user'
)
