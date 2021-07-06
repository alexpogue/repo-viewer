from flask import Blueprint, request, abort, jsonify
from ..models.repository import (
    Repository,
    repository_schema,
    repositories_schema
)
from ..models.base import db
from .util import (
    get_by_id,
    update_object_fields_by_dict,
    ensure_json_or_die,
    convert_fields_to_date
)

repository_blueprint = Blueprint('repository', __name__)


@repository_blueprint.route('/')
def get_repositories():
    all_repositories = Repository.query.all()
    return jsonify({'data': repositories_schema.dump(all_repositories)})


@repository_blueprint.route('/<int:repository_id>', methods=['GET'])
def get_repository(repository_id):
    repository = get_by_id(Repository, repository_id, repository_schema)
    return jsonify({'data': repository})


@repository_blueprint.route('/', methods=['POST'])
def new_repository():
    ensure_json_or_die()
    request_data = request.get_json()

    repository = Repository()
    update_object_fields_by_dict(repository, request_data)

    date_fields = ['created_date', 'last_push_date']
    convert_fields_to_date(repository, date_fields)

    db.session.add(repository)
    db.session.commit()
    return jsonify({'data': 'success'})


@repository_blueprint.route('/<int:repository_id>', methods=['PUT'])
def update_repository(repository_id):
    ensure_json_or_die()
    request_data = request.get_json()

    repository = Repository.query.get(repository_id)
    if repository is None:
        abort(404)

    update_object_fields_by_dict(repository, request_data)

    date_fields = ['created_date', 'last_push_date']
    convert_fields_to_date(repository, date_fields)

    db.session.commit()
    return jsonify({'data': 'success'})


@repository_blueprint.route('/<int:repository_id>', methods=['DELETE'])
def delete_repository(repository_id):
    repository = Repository.query.get(repository_id)
    if repository is None:
        abort(404)

    db.session.delete(repository)
    db.session.commit()
    return jsonify({'data': 'success'})
