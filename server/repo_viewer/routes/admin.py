import datetime
import requests
from flask import Blueprint, jsonify
from ..models.repository import Repository
from ..models.base import db

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/refresh_repo_db')
def refresh_repositories_database():
    response = requests.get('https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc')
    # check status, etc.
    json = response.json()
    repositories = convert_full_github_json_to_repositories(json)

    db.drop_all()
    db.create_all()
    for repository in repositories:
        db.session.add(repository)

    db.session.commit()
    return jsonify({'data': 'success'})

def convert_full_github_json_to_repositories(github_json):
    repos_json = github_json.get('items')
    if repos_json is None:
        return jsonify({'data': 'failure, search returned null repo list'})

    response_repos = []
    for repo_json in repos_json:
        repo = convert_single_github_repo_json_to_repository(repo_json)
        response_repos.append(repo)

    return response_repos

def convert_single_github_repo_json_to_repository(repo_json):
    github_id = repo_json.get('id')
    name = repo_json.get('name')
    url = repo_json.get('html_url')
    description = repo_json.get('description')

    created_datetime_str = repo_json.get('created_at')
    created_date = datetime_str_to_date(created_datetime_str)

    last_push_datetime_str = repo_json.get('pushed_at')
    last_push_date = datetime_str_to_date(last_push_datetime_str)

    repo_details_api_url = repo_json.get('url')
    num_stars = look_up_number_of_stars(repo_details_api_url)

    return Repository(
        github_id=github_id,
        name=name,
        url=url,
        description=description,
        created_date=created_date,
        last_push_date=last_push_date,
        num_stars=num_stars
    )

def datetime_str_to_date(datetime_str):
    my_datetime = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    return my_datetime.date()

def look_up_number_of_stars(repo_details_api_url):
    r = requests.get(repo_details_api_url)
    repo_details_json = r.json()

    num_stars = repo_details_json.get('stargazers_count')
    return num_stars
