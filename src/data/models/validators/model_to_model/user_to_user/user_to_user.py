from flask_login import current_user

from ..model_to_model import ModelToModel
from src.data.models import User
from src.config.utils import default


class UserToUser(ModelToModel):
    ABORT_MESSAGE = 'У вас нет доступа к этому пользователю'

    def __init__(self, user1, user2=None, *args, **kwargs):
        user2 = default(current_user, user2)

        models = [
            {'model': user1, 'columns': User.LOGIN_COLUMNS},
            {'model': user2, 'columns': User.LOGIN_COLUMNS}
        ]

        super().__init__(models=models, *args, **kwargs)
