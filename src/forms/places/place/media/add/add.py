from wtforms import SubmitField, MultipleFileField

from src.config.constants import FORBIDDEN_EXTENSIONS
from src.forms.form import Form
from src.validators import FileExtensions


class AddPlaceMediaForm(Form):
    folders = MultipleFileField(
        'Добавить папки', validators=[
            FileExtensions(FORBIDDEN_EXTENSIONS, must_be=False)])
    files = MultipleFileField(
        'Добавить файлы', validators=[
            FileExtensions(FORBIDDEN_EXTENSIONS, must_be=False)])
    submit = SubmitField('Сохранить')
