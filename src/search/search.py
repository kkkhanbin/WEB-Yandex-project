from .results.results import Results
from .results.__all_results import ALL_RESULTS
from src.config.utils import default


class Search:
    @classmethod
    def search(cls, text: str, searchers: list = None) -> Results:
        """
        Поиск по поисковому запросу

        Поиск осуществляется по пользователям и странам

        :param text: поисковый запрос
        :param searchers: список классов-поисковиков с функцией search и
        следующей сигнатурой:
            :param str text: поисковый запрос
            :return src.search.results.results.Results: список найденных
            результатов

            По умолчанию используются все поисковики из src.search.results
        :return: список результатов
        """

        searchers = default(searchers, ALL_RESULTS)

        # Все результаты поиска
        results = Results(text)

        # Обработка неккоректного запроса
        if len(text) < 1:
            results.errors['Short request text length'].append(
                'Слишком короткий поисковый запрос')
            return results

        for searcher in searchers:

            # Проверяем каждое слово в поисковом запросе
            for word in text.split():

                # Передаем слово поисковой функции и получаем все найденные
                # результаты, которые она нашла
                word_results = searcher.search(word)

                # Проходим по результатам
                for word_result in word_results:

                    # Если такого результата нет, то добавляем, чтобы не было
                    # повторяющихся ответов
                    if word_result not in results:
                        results.append(word_result)

        return results
