from wtforms import SelectField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange

from src.forms.form import Form


class EditMapForm(Form):
    L_TYPES_CONVERT = {
        'Карта': 'map',
        'Спутник': 'sat',
        'Гибрид': 'sat,skl'
    }

    l = SelectField(
        'Тип карты', choices=L_TYPES_CONVERT.keys(),
        validators=[DataRequired()], default='Карта')
    longitude = FloatField(
        'Долгота', default=0, validators=[
            NumberRange(-180, 180, 'Долгота должна быть между -180 и 180')])
    latitude = FloatField('Широта', default=0, validators=[
        NumberRange(-89, 89, 'Широта должна быть между -89 и 89')])
    z = IntegerField(
        'Степень приближения', default=1, validators=[
            NumberRange(
                0, 17, 'Степень приближения должна быть между 0 и 17')])
    submit = SubmitField('Обновить')
