from flask import request
from flask_wtf import FlaskForm

from .search.search import SearchForm
from .login.login import LoginForm
from .profile.edit.edit import EditProfileForm
from .profile.delete.delete import DeleteProfileForm
from .register.register import RegisterForm
from .profile.develop.apikey.add.add import AddEditApikeyForm
from .map.edit.edit import EditMapForm

# Разветвление форм для того, чтобы в будущем можно было легко разделить эти
# две формы, но сейчас они полностью идентичны, поэтому нет смысла создавать
# лишнюю форму
AddApikeyForm = EditApikeyForm = AddEditApikeyForm


def get_request_field(form: FlaskForm, field_name: str) -> str or None:
    """
    Получение текста запроса

    Поиск проходит по переданной форме или в аргументах адресной строки

    :param form: форма, обладающая полем text, из которого будет взят текст
    :param field_name: название поля, из которого вернуть значение
    :return: найденный текст или None
    """
    if field_name in request.args:
        # Обработка запроса через аргументы адресной строки
        return request.args[field_name]

    if form.validate_on_submit():
        # Обработка запроса через форму поиска
        return form.__getattribute__(field_name).data


__all__ = (
    'SearchForm', 'LoginForm', 'EditProfileForm', 'AddApikeyForm',
    'DeleteProfileForm', 'RegisterForm', 'EditApikeyForm', 'EditWorldMapForm',
    'get_request_field'
)
