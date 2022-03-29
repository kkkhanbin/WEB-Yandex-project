from flask import redirect
from flask_login import logout_user

from src.routes import routes_bp


@routes_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')
