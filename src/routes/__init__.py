# Blueprint
from flask import Blueprint
routes_bp = Blueprint('routes', __name__, template_folder='templates')

# routes
from .index import index
from .favicon.favicon import favicon
from .register.register import register
from .logout import logout
from .login import login

__all__ = (
    'routes_bp', 'index', 'favicon', 'register', 'logout', 'login'
)
