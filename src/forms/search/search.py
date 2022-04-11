from wtforms import StringField
from wtforms.validators import DataRequired, Length

from src.forms.form import Form


class SearchForm(Form):
    text = StringField('Введите запрос', validators=[
        DataRequired(), Length(1, 200, 'Слишком длинный запрос')])
