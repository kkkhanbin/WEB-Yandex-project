from wtforms import SubmitField, MultipleFileField

from src.config import config
from src.forms.form import Form
from src.validators import FileExtensions


class AddPlaceMediaForm(Form):
    folders = MultipleFileField(
        'Добавить папки', validators=[
            FileExtensions(config.FORBIDDEN_EXTENSIONS, must_be=False)])
    files = MultipleFileField(
        'Добавить файлы', validators=[
            FileExtensions(config.FORBIDDEN_EXTENSIONS, must_be=False)])
    submit = SubmitField('Сохранить')
