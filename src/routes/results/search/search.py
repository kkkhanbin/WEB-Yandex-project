from src.data import session
from src.data.models import User
from .result_types import USER_RESULT_TYPE
from .results import Result, Results


class Search:
    @classmethod
    def search(cls, text: str) -> Results or dict:
        """
        Поиск по тексту

        Поиск осуществляется по пользователям и странам

        :param text: поисковый запрос
        :return: список результатов или dict - ошибку
        """
        # Все результаты поиска
        results = Results(text)

        # Обработка неккоректного запроса
        if len(text) < 1:
            results.errors['Short request text length'].append(
                'Слишком короткий поисковый запрос')
            return results

        # Поисковые функции, которые будут выполнятся при общем поиске со след.
        # сигнатурой:
        # :param text: поисковый запрос. Тип - str
        # :return: список результатов. Тип - Results
        search_functions = [cls.search_users]
        for search_func in search_functions:
            # Проверяем каждое слово в поисковом запросе
            for word in text.split():
                # Передаем слово поисковой функции и получаем все найденные
                # результаты, которые она нашла
                word_results = search_func(word)

                # Проходим по результатам
                for word_result in word_results:
                    # Если такого результата нет, то добавляем, чтобы не было
                    # повторяющихся ответов
                    if word_result.model not in \
                            [result.model for result in results]:
                        results.append(word_result)

        return results

    @classmethod
    def search_users(cls, text: str) -> Results:
        # Поиск пользователей по никнейму, имени и фамилии
        users = session.query(User).filter(
            User.nickname.like(f'%{text}%') |
            User.name.like(f'%{text}%') |
            User.surname.like(f'%{text}%')).distinct().all()

        return cls.pack_models_in_results(text, users, USER_RESULT_TYPE)

    @classmethod
    def pack_models_in_results(
            cls, text, models, type) -> Results:
        """
        Упаковывает ORM-модели в список результатов Results

        :param text: поисковый запрос для инициализации Results
        :param models: ORM-модели, которые нужно упаковать
        :param type: тип результата. См. search/result_types
        :return: полученный список результатов Results
        """

        results = Results(text)
        for model in models:
            results.append(Result(type, {'model': model}))
        return results
