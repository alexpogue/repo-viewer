from .repository import repository_blueprint
from .root_api import root_api_blueprint


def init_app(app):
    app.register_blueprint(repository_blueprint, url_prefix='/repo')
    app.register_blueprint(
        root_api_blueprint,
        url_prefix='/',
        template_folder='../templates',
        static_folder='../static'
    )
