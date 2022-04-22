from flask import abort
from flask_login import current_user
from werkzeug.exceptions import Forbidden

from ..validator import Validator


class UserToUser(Validator):
    """
    Проверка доступа пользователя user_from к пользователю user_to
    """

    ABORT_MESSAGE = 'У вас нет доступа к этому пользователю'

    def __init__(self, user_to, user_from=None, *args, **kwargs) -> None:
        """
        :param user_to: к какому пользователю проверить доступ
        :param user_from: от какого пользователя проверить доступ.
        По умолчанию текущий
        """

        super().__init__(*args, **kwargs)

        if user_from is None:
            user_from = current_user

        self.user_from = user_from
        self.user_to = user_to

    def __call__(self) -> None:
        # Если это разные люди, тогда доступа нет
        if not self.user_from.check_login(self.user_to.nickname):
            abort(Forbidden.code, description=self.message)
