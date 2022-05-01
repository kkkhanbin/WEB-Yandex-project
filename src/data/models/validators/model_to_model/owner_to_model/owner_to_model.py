from flask_login import current_user

from ..model_to_model import ModelToModel
from src.config.utils import default


class OwnerToModel(ModelToModel):
    ABORT_MESSAGE = 'У вас нет доступа'

    def __init__(self, model, owner_column: str = 'owner',
                 user=None, *args, **kwargs):
        user = default(user, current_user)

        models = [
            {'model': user, 'columns': ['id']},
            {'model': model, 'columns': [owner_column]}
        ]

        super().__init__(models=models, *args, **kwargs)
