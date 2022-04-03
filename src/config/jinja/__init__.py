from jinja2 import Environment

from .tests.tests import file_exists


def add_tests(env: Environment, tests: dict) -> None:
    """
    Добавляет jinja тесты в среду

    :param env: jinja2.Environment - среда, в которую нужно добавлять тесты
    :param tests: dict, состоящий из тестов для добавления
    :return: None
    """
    for test_name in tests:
        env.tests[test_name] = tests[test_name]


TESTS = {
    'file_exists': file_exists
}

__all__ = (
    'TESTS', 'add_tests'
)
