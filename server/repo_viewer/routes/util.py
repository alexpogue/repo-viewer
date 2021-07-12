import datetime
from flask import abort, request
from flask import current_app as app


def ensure_json_or_die():
    if not request.is_json:
        app.logger.info(
            'Error: {} {} only supports Content-Type: application/json'.format(
                request.method,
                request.path
            )
        )
        abort(415, {'message': 'Expected Content-Type: application/json'})


def get_by_id(model_cls, lookup_id, schema):
    model_obj = model_cls.query.get(lookup_id)
    if model_obj is None:
        abort(404)
    result = schema.dump(model_obj)

    return result


def update_object_fields_by_dict(obj, dic):
    for field, value in dic.items():
        if hasattr(obj, field):
            setattr(obj, field, value)


def python_date_from_string(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


def convert_fields_to_date(obj, date_fields):
    for field in date_fields:
        if hasattr(obj, field):
            date = getattr(obj, field)
            if isinstance(date, str):
                setattr(obj, field, python_date_from_string(date))


def get_github_user_request_headers(user_token):
    if user_token is None:
        return None

    headers = {"Authorization": "Token {}".format(user_token),
               "Accept": "application/vnd.github.v3+json"}

    return headers
