from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from src.forms.form import Form


class AddEditApikeyForm(Form):
    name = StringField(
        f'Название API-ключа, никак не влияет на сам ключ, '
        f'нужно только для удобства')
    access_level = SelectField(
        'Уровень доступа*', validators=[
            DataRequired('Нужно указать уровень доступа')],
        validate_choice=False)
    submit = SubmitField('Сохранить')
