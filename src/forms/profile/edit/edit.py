from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, EmailField, BooleanField, \
    FileField
from wtforms.validators import DataRequired, Length

from src.data.models import User
from src.forms.validators import Unique
from src.forms.form import Form

MIN_PASSWORD_LENGTH = 10


class EditProfileForm(Form):
    avatar_image = FileField(
        'Фото профиля',
        validators=[FileAllowed(['jpg', 'png', 'svg', 'jpeg', 'bmp'],
                                'Разрешены только картинки')])
    nickname = StringField('Ник*', validators=[
        DataRequired(), Unique(User, message='Такой никнейм уже существует')])
    email = EmailField(
        'Почта*', validators=[
            DataRequired(), Unique(
                User, message='Такой емейл уже существует')])
    surname = StringField(
        'Фамилия', validators=[
            Length(0, 50, 'Фамилия не должна превышать длину в 50 символов')])
    name = StringField(
        'Имя', validators=[
            Length(0, 50, 'Имя не должно превышать длину в 50 символов')])
    login = BooleanField('Войти', default=True)
    submit = SubmitField('Сохранить')
