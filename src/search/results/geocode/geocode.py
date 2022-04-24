from src.search import Results, Result
from src.api import Geocoder


class GeocodeResult(Result):
    TEMPLATE_PATH = Result.TEMPLATES_TYPES_PATH + 'geocode/geocode.html'

    @classmethod
    def search(cls, text: str) -> Results:
        response = Geocoder.get({'geocode': text, 'format': 'json'})
        features = Geocoder.get_features(response)

        return cls.pack_results(
            text, features, lambda feature: cls({'feature': feature}))
