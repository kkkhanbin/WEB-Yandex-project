from flask import abort
from werkzeug.exceptions import Forbidden

from ..validator import Validator


class Blocked(Validator):
    ABORT_MESSAGE = 'Страница заблокирована'

    def __init__(self, model, *args, **kwargs) -> None:
        """
        :param model: ORM-модель, обязана обладать колонкой block
        """

        super().__init__(*args, **kwargs)

        self.model = model

    def __call__(self) -> None:
        if self.model.block:
            abort(Forbidden.code, description=self.message)
