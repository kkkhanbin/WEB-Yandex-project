from flask import abort
from werkzeug.exceptions import Forbidden

from ..validator import Validator


class UserToApikey(Validator):
    ABORT_MESSAGE = 'У вас нет доступа к этому API-ключу'

    def __init__(self, user, apikey, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.user = user
        self.apikey = apikey

    def __call__(self) -> None:
        if self.apikey.owner != self.user.id:
            abort(Forbidden.code, description=self.message)
