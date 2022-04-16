from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, EmailField, BooleanField, \
    PasswordField, FileField
from wtforms.validators import DataRequired, Length, EqualTo

from src.data.models import User
from src.forms.validators import Unique
from src.forms.form import Form

MIN_PASSWORD_LENGTH = 10


class AddEditProfileForm(Form):
    avatar_image = FileField(
        'Фото профиля',
        validators=[FileAllowed(['jpg', 'png', 'svg', 'jpeg', 'bmp'],
                                'Разрешены только картинки')])
    nickname = StringField('Ник', validators=[
        DataRequired(), Unique(User, message='Такой никнейм уже существует')])
    email = EmailField(
        'Почта', validators=[
            DataRequired(), Unique(User, message='Такой емейл уже существует')])
    password = PasswordField('Пароль', validators=[
        DataRequired('Нужно ввести пароль'),
        Length(MIN_PASSWORD_LENGTH, message=
        f'Минимальная длина пароля - {MIN_PASSWORD_LENGTH} символов')])
    repeat_password = PasswordField(
        'Повторите пароль', validators=[
            DataRequired('Нужно снова ввести пароль'),
            Length(MIN_PASSWORD_LENGTH, message=
            f'Минимальная длина пароля - {MIN_PASSWORD_LENGTH} символов'),
            EqualTo('password', 'Пароли не совпадают')])
    surname = StringField(
        'Фамилия', validators=[
            Length(0, 50, 'Фамилия не должна превышать длину в 50 символов')])
    name = StringField(
        'Имя', validators=[
            Length(0, 50, 'Имя не должно превышать длину в 50 символов')])
    login = BooleanField('Войти', default=True)
    submit = SubmitField('Сохранить')
