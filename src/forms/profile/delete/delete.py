from wtforms import StringField, SubmitField, BooleanField

from src.forms.form import Form
from src.validators import EqualToValue


class DeleteProfileForm(Form):
    CONFIRM_WORD = 'ПОДТВЕРДИТЬ'

    confirm_word = StringField(
        f'Напишите слово "{CONFIRM_WORD}" для удаления аккаунта*',
        validators=[EqualToValue(
            CONFIRM_WORD, message='Слово подтверждения неправильное')])
    confirm = BooleanField(
        'Вы уверены?*', default=False,
        validators=[EqualToValue(
            True, message='Нажмите кнопку "Вы уверены?" для удаления')])
    submit = SubmitField('Удалить профиль')
