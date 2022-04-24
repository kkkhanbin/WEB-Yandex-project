from .geocode.geocode import GeocodeResult
from .user.user import UserResult

ALL_RESULTS = [GeocodeResult, UserResult]

__all__ = (
    'UserResult', 'GeocodeResult', 'ALL_RESULTS'
)
