from flask_login import login_required

from src.routes import routes_bp


@routes_bp.route('/profile/<login>')
def profile(login):
    pass
