import datetime
import requests
from flask import Blueprint, jsonify, current_app as app, request
from ..models.repository import Repository
from ..models.base import db
from .util import get_github_user_request_headers

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/refresh_repo_db', methods=['POST'])
def refresh_repositories_database():
    token = request.args.get('token')
    if token is not None:
        app.logger.info('Using token: {}'.format(token))
    else:
        app.logger.info('not using token')

    path_query = 'q=language:python&sort=stars&order=desc'
    path = 'https://api.github.com/search/repositories?{}'.format(path_query)

    headers = get_github_user_request_headers(token)

    response = requests.get(path, headers=headers)
    # check status, etc.
    response_json = response.json()

    try:
        repositories = convert_full_github_json_to_repositories(
            response_json,
            token
        )

        db.drop_all()
        db.create_all()
        for repository in repositories:
            db.session.add(repository)

        db.session.commit()
        return jsonify({'data': 'success'})
    except RuntimeError as e:
        reason = str(e)
        return_code = 500
        if 'API rate limit exceeded' in reason:
            return_code = 429
        return jsonify({'data': 'fail', 'reason': reason}), return_code


@admin_blueprint.route('/github_client_id', methods=['GET'])
def get_github_client_id():
    return jsonify({'data': app.config.get('GITHUB_APP_CLIENT_ID')})


def convert_full_github_json_to_repositories(github_json, token):
    """Convert all repositories in dictionary to Repository model object array.

    :param dict github_json: Repos data from /search/repositories Github API
    :raise: RuntimeError if any db fields were not present in input param.
    :return: Repository object array
    :rtype: array
    """

    repos_json = github_json.get('items')
    if repos_json is None:
        return jsonify({'data': 'failure, search returned null repo list'})

    response_repos = []
    for repo_json in repos_json:
        repo = convert_single_github_repo_json_to_repository(repo_json, token)
        response_repos.append(repo)

    return response_repos


def convert_single_github_repo_json_to_repository(repo_json, token):
    """Convert one repository dictionary to a Repository model object.

    :param dict repo_json: Repo data from /search/repositories Github API
    :raise: RuntimeError if any db fields were not present in API response.
    :return: One Repository object
    :rtype: dict
    """

    created_datetime_str = repo_json.get('created_at')
    created_date = datetime_str_to_date(created_datetime_str)

    last_push_datetime_str = repo_json.get('pushed_at')
    last_push_date = datetime_str_to_date(last_push_datetime_str)

    # description can be "null" instead of undefined in API response. Handle it
    description_from_api = repo_json.get('description', '')
    description = '' if description_from_api is None else description_from_api

    repo_details_api_url = repo_json.get('url')
    num_stars = look_up_number_of_stars(repo_details_api_url, token)

    repo_obj = {
        'github_id': repo_json.get('id'),
        'name': repo_json.get('name'),
        'url': repo_json.get('html_url'),
        'description': description,
        'created_date': created_date,
        'last_push_date': last_push_date,
        'num_stars': num_stars
    }

    for key, value in repo_obj.items():
        if value is None:
            repo_name = repo_obj.get('name')
            msg = 'In API, could not find {} - repo: {}'.format(key, repo_name)
            raise RuntimeError(msg)

    return Repository(**repo_obj)


def datetime_str_to_date(datetime_str):
    dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    return dt.date()


def look_up_number_of_stars(repo_details_api_url, token):
    app.logger.info('repo_details_api_url = {}'.format(repo_details_api_url))

    headers = get_github_user_request_headers(token)
    r = requests.get(repo_details_api_url, headers=headers)

    repo_details_json = r.json()
    if r.status_code != 200:
        error_msg = 'Could not get num_stars, status: {}'.format(r.status_code)
        if 'API rate limit exceeded' in repo_details_json.get('message'):
            error_msg += ' API rate limit exceeded.'
        raise RuntimeError(error_msg)

    num_stars = repo_details_json.get('stargazers_count')
    return num_stars
