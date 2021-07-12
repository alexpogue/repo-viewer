import requests
from flask import Blueprint, jsonify, current_app as app, request

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/token', methods=['GET'])
def get_user_github_token():
    client_id = app.config.get('GITHUB_APP_CLIENT_ID')
    client_secret = app.config.get('GITHUB_APP_CLIENT_SECRET')
    code = request.args.get('code')

    r = requests.post(
        'https://github.com/login/oauth/access_token',
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code
        },
        headers={
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    app.logger.info('r = {}'.format(r.text))

    access_token = r.json().get('access_token')

    return jsonify({'data': access_token})
