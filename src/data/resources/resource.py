from abc import abstractmethod

from flask_restful import Resource, reqparse


class RestResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @staticmethod
    @abstractmethod
    def add_arguments(parser: reqparse.RequestParser) -> None:
        """
        Добавление аргументов в парсер реквеста ресурса

        :param parser: парсер, в который нужно добавить аргументы
        :return: None
        """
        pass
