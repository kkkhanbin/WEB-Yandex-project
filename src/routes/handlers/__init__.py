# Blueprint
from flask import Blueprint
handlers_bp = Blueprint('handlers', __name__)

# handlers
from .not_found.not_found import not_found
from .forbidden.forbidden import forbidden
from .unauthorized.unauthorized import unauthorized

__all__ = (
    'not_found', 'forbidden', 'unauthorized'
)
