from abc import abstractmethod, ABC

from flask import render_template

from src.search.results.results import Results


class Result(ABC):
    """
    Результат поискового запроса
    """

    TEMPLATES_TYPES_PATH = 'results/types/'

    def __init__(self, content: dict) -> None:
        self.content = content

    @classmethod
    @abstractmethod
    def search(cls, text: str) -> Results:
        """
        Процесс поиска по тексту

        :param text: поисковая строка
        :return: src.search.Results
        """

    @classmethod
    def pack_results(
            cls, text: str, values: list, convert_func, *args, **kwargs) \
            -> Results:
        """
        Упаковка каждого найденного объекта в Result, а затем в Results

        Универсальная функция упаковки, в дочерних классах, при надобности
        можно переопределять. Эта функция нужна только для устранения
        дублирования

        :param text: поисковая строка, по которой искались объекты
        :param values: найденные объекты для упаковки
        :param convert_func: функция для конвертирования информации,
        полученной в аргументах, в src.search.results.result.Result со
        следующей сигнатурой:
            :param value: значение для конвертирования
            :param *args: любые позиционные аргументы
            :param **kwargs: любые именованные аргументы
            :return: src.search.results.result.Result

        :return: src.search.Results
        """

        results = Results(text)
        for value in values:
            results.append(convert_func(value, *args, **kwargs))
        return results

    @property
    def html(self) -> str:
        """
        Получение html-кода результата запроса

        Позволяет более гибко настраивать показ результата поиска

        :return str: html-код результата запроса
        """

        return render_template(self.TEMPLATE_PATH, content=self.content)
