from flask import abort
from werkzeug.exceptions import NotFound

from ..validator import Validator


class ModelNotFound(Validator):
    ABORT_MESSAGE = 'Страница не найдена'

    def __init__(self, model, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.model = model

    def __call__(self) -> None:
        if self.model is None or \
                (isinstance(self.model, list) and len(self.model) == 0):
            abort(NotFound.code, description=self.message)
