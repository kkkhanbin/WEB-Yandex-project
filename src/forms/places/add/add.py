from wtforms import StringField, SubmitField, FloatField, IntegerField, \
    MultipleFileField, TextAreaField

from src.forms.form import Form


class AddEditPlaceForm(Form):
    name = StringField(
        'Название места (его географическое название, которое будет '
        'использоваться для поиска координат)')
    description = TextAreaField('Описание')
    media = MultipleFileField('Любые медиа-файлы')

    submit = SubmitField('Сохранить')

    owner = IntegerField()
    lon = FloatField()
    lat = FloatField()
