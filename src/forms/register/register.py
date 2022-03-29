from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, SelectMultipleField,\
    BooleanField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileAllowed

from src.data.models import Country, User
from src.data import session
from src.forms.validators import Unique


class RegisterForm(FlaskForm):
    COUNTRIES = [country.name for country in session.query(Country).all()]

    nickname = StringField('Ник', validators=[
        DataRequired(), Unique(User, 'Такой никнейм уже существует')])
    email = EmailField(
        'Почта', validators=[
            DataRequired(), Unique(User, 'Такой емейл уже существует')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField(
        'Повторите пароль', validators=[
            DataRequired(), EqualTo('password', 'Пароли не совпадают')])
    surname = StringField(
        'Фамилия', validators=[
            Length(0, 50, 'Фамилия не должна превышать длину в 50 символов')])
    name = StringField(
        'Имя', validators=[
            Length(0, 50, 'Имя не должно превышать длину в 50 символов')])
    countries = SelectMultipleField('Посещенные страны', choices=COUNTRIES)
    avatar_image = FileField(
        'Фото профиля',
        validators=[FileAllowed(['jpg', 'png', 'svg'],
                                'Разрешены только картинки')])
    login = BooleanField('Войти', default=True)
    submit = SubmitField('Зарегистрироваться')
