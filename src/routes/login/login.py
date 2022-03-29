from flask import render_template
from flask_login import current_user, login_user

from src.routes import routes_bp
from src.forms import SearchForm, LoginForm


@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    search_form = SearchForm()

    if