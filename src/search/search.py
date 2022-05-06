import logging

from .results.results import Results
from .results.__all_results import ALL_RESULTS
from src.config.utils import default


class Search:
    TOO_SHORT_REQ_LENGTH_ID = 'Short request text length'
    TOO_SHORT_REQ_LENGTH_MESSAGE = 'Слишком короткий поисковый запрос'

    @classmethod
    def search(cls, text: str, searchers: list = None) -> Results:
        """
        Поиск по поисковому запросу

        Поиск осуществляется по пользователям и странам

        :param text: поисковый запрос
        :param searchers: список классов-поисковиков с функцией search. По
        умолчанию используются все поисковики из src.search.results
        :return: список результатов
        """

        logging.info(f'Был произведен поиск по запросу: {text}')

        searchers = default(searchers, ALL_RESULTS)

        # Все результаты поиска
        results = Results(text)

        # Обработка неккоректного запроса
        if len(text) < 1:
            logging.error(f'При поиске по запросу: {text} произошла ошибка: '
                          f'{cls.TOO_SHORT_REQ_LENGTH_MESSAGE}')
            results.errors[cls.TOO_SHORT_REQ_LENGTH_ID].append(
                cls.TOO_SHORT_REQ_LENGTH_MESSAGE)
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
