from src.routes import routes_bp


@routes_bp.route('/profile/<nickname>')
def profile(nickname):
    pass
