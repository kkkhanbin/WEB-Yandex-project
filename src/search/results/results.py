from collections import defaultdict


class Results(list):
    """
    Список результатов поисковых запросов
    """

    def __init__(self, request_text: str, *args, **kwargs):
        """
        Инициализация списка результатов

        :param request_text: поисковый текст
        """

        self.request_text = request_text
        self.errors = defaultdict(list)

        super().__init__(*args, **kwargs)
