from flask import abort
from werkzeug.exceptions import Forbidden

from ..validator import Validator


class AccessLevel(Validator):
    ABORT_MESSAGE = 'Не хватает уровня доступа'

    def __init__(self, model, req_access_level: int, *args, **kwargs) -> None:
        """
        :param model: ORM-модель, обязана быть колонка access_level
        :param req_access_level: требуемый уровень доступа, если уровень
        доступа ниже, создастся ошибка
        :return: None
        """

        super().__init__(*args, **kwargs)

        self.model = model
        self.req_access_level = req_access_level

    def __call__(self) -> None:
        if self.model.access_level < self.req_access_level:
            abort(Forbidden.code, description=self.message)
