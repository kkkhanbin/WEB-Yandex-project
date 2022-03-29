from src.routes import routes_bp


@routes_bp.route('/results', methods=['GET', 'POST'])
def results():
    pass
