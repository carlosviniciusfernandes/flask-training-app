from quart import Quart

from .reviews import reviews_bp
from .users import users_bp


def register_blueprints(app: Quart):
    app.register_blueprint(reviews_bp)
    app.register_blueprint(users_bp)
