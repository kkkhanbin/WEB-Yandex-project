from flask import abort
from werkzeug.exceptions import Forbidden

from ..validator import Validator
from src.config.utils import default


class ModelToModel(Validator):
    """
    Проверка равенства колонок моделей

    Хотя бы одна пара значений всех переданных колонок моделей должна быть
    равна друг другу. Валидатор проверяет каждую переданную колонку и
    сравнивает ее со всеми остальными

    Например:
    Проверка доступа пользователя к API-ключу
        models=[{'model': User(), 'columns': ['id']},
                {'model': Apikey(), 'columns': ['owner'}]]
    В данном случае валидатор проверит значения User.id == Apikey.owner и если
    они не равны, вернет ошибку

    """

    ABORT_MESSAGE = 'У вас нет доступа к этой странице'

    def __init__(
            self, models: list = None, *args,
            **kwargs) -> None:
        """
        :param models: список моделей в виде:
            [{'model': User(), 'columns': ['id']},
             {'model': Apikey(), 'columns': ['owner'}]]
            Их можете быть неограниченное количество
        """

        super().__init__(*args, **kwargs)

        models = default(models, [])

        self.models = models

    def __call__(self) -> None:
        success = False
        # Проходим по всем моделям кроме первой чтобы на каждой итерации
        # проверять по две модели
        for i in range(len(self.models[1:])):
            model1, model2 = self.models[i - 1], self.models[i]

            # Здесь сравнивается каждая колонка модели 1 с каждой колонкой
            # модели 2
            for column1 in model1['columns']:
                for column2 in model2['columns']:

                    # Если хоть одно значение совпадает, то валидация прошла
                    # успешно
                    if getattr(model1['model'], column1) == \
                            getattr(model2['model'], column2):
                        success = True

        if not success:
            abort(Forbidden.code, description=self.message)
