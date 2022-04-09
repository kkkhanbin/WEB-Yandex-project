from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired

from src.forms.form import Form


class LoginForm(Form):
    login = StringField('Ник, id или почту', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Войти')
