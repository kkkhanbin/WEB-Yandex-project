# Blueprint
from flask import Blueprint
handlers_bp = Blueprint('handlers', __name__)

# handlers
from .not_found.not_found import not_found
from .forbidden.forbidden import forbidden
from .unauthorized.unauthorized import unauthorized
from .request_entity_too_large.request_entity_too_large import \
    request_entity_too_large
from .bad_request.bad_request import bad_request

__all__ = (
    'not_found', 'forbidden', 'unauthorized', 'request_entity_too_large',
    'bad_request'
)
