from flask import abort
from flask_login import current_user
from werkzeug.exceptions import Unauthorized

from ..validator import Validator
from src.config.utils import default


class UserUnauthorized(Validator):
    ABORT_MESSAGE = 'Вы не авторизованы'

    def __init__(self, user=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.user = default(user, current_user)

    def __call__(self) -> None:
        if not self.user.is_authenticated:
            abort(Unauthorized.code, description=self.message)
