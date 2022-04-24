from flask_restful import reqparse
from email_validator import validate_email

from src.data.models import User
from src.validators import Unique, ArgumentValidator


class UserDataParser(reqparse.RequestParser):
    UNIQUE_COLUMNS = ['id', 'nickname', 'email']

    def __init__(self, default_id: int = None, except_values: dict = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        if except_values is None:
            except_values = {}
            for column in self.UNIQUE_COLUMNS:
                except_values[column] = []

        unique_args = [
            ('id', {'required': False, 'default': default_id}, []),
            ('nickname', {'required': True}, []),
            ('email', {'required': True}, [validate_email])
        ]

        for arg_name, unique_kwargs, validators in unique_args:
            self.add_argument(
                arg_name, **unique_kwargs,
                type=ArgumentValidator(Unique(
                    User, column_name=arg_name,
                    type=Unique.VALIDATION_ARGUMENT_TYPE,
                    except_values=except_values[arg_name]), *validators))

        self.add_argument('password', required=True)
        self.add_argument('surname', required=False)
        self.add_argument('name', required=False)
