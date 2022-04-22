from flask_restful import reqparse


class ApikeyParser(reqparse.RequestParser):
    def __init__(self):
        super().__init__()

        self.add_argument('apikey', required=True, location='args')
