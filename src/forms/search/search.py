from wtforms import StringField
from wtforms.validators import DataRequired

from src.forms.form import Form


class SearchForm(Form):
    text = StringField('Введите запрос', validators=[DataRequired()])
