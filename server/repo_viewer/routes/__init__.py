from .repository import repository_blueprint
from .admin import admin_blueprint
from .user import user_blueprint
from .root_api import root_api_blueprint


def init_app(app):
    app.register_blueprint(repository_blueprint, url_prefix='/api/repo')
    app.register_blueprint(admin_blueprint, url_prefix='/api/admin')
    app.register_blueprint(user_blueprint, url_prefix='/api/user')
    app.register_blueprint(
        root_api_blueprint,
        url_prefix='/',
        template_folder='../templates',
        static_folder='../static'
    )
