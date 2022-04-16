from collections import defaultdict

from flask import render_template

from .result_types import USER_RESULT_TYPE

TYPES_PATH = 'results/types/'
# html шаблоны для разных типов результатов поиска
HTML_TEMPLATES = {
    USER_RESULT_TYPE: TYPES_PATH + 'user/user.html'
}


class Result:
    def __init__(self, type, content: dict):
        """
        Инициализация результата поиска

        :param type: тип ответа. См. search/result_types
        :param content: словарь с содержанием результата. Обязательные ключи:
        model - ORM-модель результата
        """

        self.type = type
        self.content = content

    @property
    def html(self) -> str:
        """
        Получение html кода результата запроса

        Позволяет более гибко настраивать показ результата поиска

        :return:
        """
        return render_template(HTML_TEMPLATES[self.type], content=self.content)

    @property
    def model(self):
        return self.content['model']


class Results(list):
    def __init__(self, request_text: str, *args, **kwargs):
        """
        Инициализация списка результатов

        :param request_text: поисковый текст
        """
        self.request_text = request_text
        self.errors = defaultdict(list)
        super(Results).__init__(*args, **kwargs)
