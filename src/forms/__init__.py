import os

from wtforms import Field
from werkzeug.utils import secure_filename

from .search.search import SearchForm
from .login.login import LoginForm
from .profile.edit.edit import EditProfileForm
from .profile.delete.delete import DeleteProfileForm
from .register.register import RegisterForm

ALLOWED_EXTENSIONS = {'png', 'jpg', 'svg'}
UPLOAD_DIR_PATH = ['upload']
AVATAR_IMAGE_PATH = \
    UPLOAD_DIR_PATH + ['/profiles/{user_id}', 'avatar.{image_extension}']


def allowed_file(filename, allowed_extensions=None) -> bool:
    """
    Проверка расширения файла

    :param filename: название фалйа
    :param allowed_extensions: допустимые расширения, по умолчанию используется
     константа ALLOWED_EXTENSIONS
    :return: bool, True - файл в списке, False - не в списке
    """
    if allowed_extensions is None:
        allowed_extensions = ALLOWED_EXTENSIONS
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_image(field: Field, path: list or str) -> bool:
    """
    Сохранение картинки из поля

    :param field: wtforms.Field, откуда нужно будет брать картинку
    :param path: путь к директории, в которой нужно сохранить файл.
    Если тип - список, тогда используется функция os.path.join для ее
    преобразования, а если строка, аргумент используется без изменений
    :return: bool, True - в случае успешного сохранения,
    False - в случае ошибки
    """
    if isinstance(path, list):
        path = os.path.join(*path)

    file = field.data
    # Если было передано фото профиля и его расширение разрешено
    if file and allowed_file(file.filename):
        # Функция secure_filename нужна для проверки названия файла на
        # высокоуровневые пути и его преобразования
        filename = secure_filename(file.filename)
        file.save(os.path.join(path, filename))
        return True
    return False


__all__ = (
    'SearchForm', 'LoginForm', 'EditProfileForm', 'save_image',
    'allowed_file', 'ALLOWED_EXTENSIONS', 'UPLOAD_DIR_PATH',
    'AVATAR_IMAGE_PATH', 'DeleteProfileForm', 'RegisterForm'
)
