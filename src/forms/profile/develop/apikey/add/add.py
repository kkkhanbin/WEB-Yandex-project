from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

from src.forms.form import Form


class AddEditApikeyForm(Form):
    name = StringField(
        'Название API-ключа, никак не влияет на сам ключ, нужно только для '
        'удобства')
    access_level = SelectField(
        'Уровень доступа*', validators=[
            DataRequired('Нужно указать уровень доступа')],
        validate_choice=False)
    apikey = StringField()
    owner = IntegerField()
    submit = SubmitField('Сохранить')
