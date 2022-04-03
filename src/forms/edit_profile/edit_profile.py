from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField


class EditProfileForm(FlaskForm):
    avatar_image = FileField(
        'Фото профиля',
        validators=[FileAllowed(['jpg', 'png', 'svg'],
                                'Разрешены только картинки')])
