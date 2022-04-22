from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

from src.forms.form import Form


class EditWorldMapForm(Form):
    l = SelectField(
        'Тип карты', choices=['map', 'sat', 'sat,skl'],
        validators=[DataRequired()])
    submit = SubmitField('Обновить')
