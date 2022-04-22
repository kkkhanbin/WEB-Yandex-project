from flask_restful import Api

from src.data.resources import UserResource, UsersListResource


def add_resources(api: Api, *resources) -> None:
    """
    Добавляет ресурсы в Api

    :param api: Экземпляр класса flask_restful.Api, которому будут добавляться
            ресурсы
    :param resources: Коллекция, где первое значение - добавляемый ресурс,
            а второе - его url
    :return: None
    """

    for resource, route in resources:
        api.add_resource(resource, route)


# Ресурсы для API в виде кортежей, где первый элемент - сам ресурс, а второй -
# его url
RESOURCES = (
    (UserResource, '/api/user/<login>'),
    (UsersListResource, '/api/users')
)

__all__ = (
    'add_resources', 'RESOURCES'
)
