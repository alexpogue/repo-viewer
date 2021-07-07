from flask import Blueprint, render_template

root_api_blueprint = Blueprint('root_api', __name__)


@root_api_blueprint.route('/')
def get_repositories():
    return render_template('gen/index.html')
