import os

from .api import Api, UseApikey
from .static.static import Static as StaticApi
from .geocoder.geocoder import Geocoder as GeocoderApi

# Инициализация API хендлеров
Static = StaticApi(os.getenv('STATIC_APIKEY'))
Geocoder = GeocoderApi(os.getenv('GEOCODER_APIKEY'))

__all__ = (
    'Api', 'StaticApi', 'Static', 'Geocoder', 'GeocoderApi', 'UseApikey'
)
