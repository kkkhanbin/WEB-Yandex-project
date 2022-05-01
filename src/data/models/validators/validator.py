from abc import abstractmethod

from src.config.utils import default


class Validator:
    """
    Валидатор моделей
    """

    # Дефолтное сообщение при провале валидации
    ABORT_MESSAGE = 'Произошла ошибка'

    @abstractmethod
    def __init__(self, message=None) -> None:
        message = default(message, self.ABORT_MESSAGE)

        self.message = message

    @abstractmethod
    def __call__(self) -> None:
        """
        Процесс валидации

        Функция ничего не получает, так как все нужные данные уже были
        получены при инициализации
        :return: None
        """

        pass
