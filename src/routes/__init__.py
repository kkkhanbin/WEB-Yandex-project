# Blueprint
from flask import Blueprint
routes_bp = Blueprint('routes', __name__, template_folder='templates')

# routes
from .index import index
from .favicon.favicon import favicon
from .register.register import register
from .logout.logout import logout
from .login.login import login
from .profile import profile
from .profile.edit.edit import edit as profile_edit
from .results.results import results
from .about.about import about
from .profile.delete.delete import delete as profile_delete
from .profile.develop.develop import develop
from .profile.develop.apikey.delete.delete import apikey_delete
from .profile.develop.apikey.add.add import apikey_add
from .profile.develop.apikey.edit.edit import apikey_edit

__all__ = (
    'routes_bp', 'index', 'favicon', 'register', 'logout', 'login', 'profile',
    'profile_edit', 'results', 'about', 'profile_delete', 'develop',
    'apikey_delete', 'apikey_add', 'apikey_edit'
)
