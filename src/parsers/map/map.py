from flask_restful import reqparse

from src.validators import ArgumentValidator, Range


class MapParser(reqparse.RequestParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_argument(
            'lon',
            required=False,
            location='args',
            type=ArgumentValidator(
                Range(-180, 180)),
            default=0
        )

        self.add_argument(
            'lat',
            required=False,
            location='args',
            type=ArgumentValidator(
                Range(-90, 90)),
            default=0
        )

        self.add_argument(
            'z',
            required=False,
            location='args',
            type=int,
            default=1,
            choices=[i for i in range(0, 18)]
        )

        self.add_argument(
            'l',
            required=False,
            location='args',
            choices=['sat', 'map', 'sat,skl'],
            default='sat'
        )

        self.add_argument(
            'pt',
            required=False,
            location='args',
            default=[]
        )
