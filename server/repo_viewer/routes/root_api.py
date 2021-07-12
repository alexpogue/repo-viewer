from flask import Blueprint, render_template, current_app as app

root_api_blueprint = Blueprint('root_api', __name__)


# Pass all unrecognized routes on to Vue (link to index). This ensures that
# localhost:8080/repos/1 isn't caught by flask which would return a 404.
@root_api_blueprint.route('/', defaults={'u_path': ''})
@root_api_blueprint.route('/<path:u_path>')
def get_repositories(u_path):
    return render_template('gen/index.html')


# Below three methods are a hack.. Explanation:
# When vue.config.js had `publicPath: '/static/gen'`, two things would happen:
#   1. Clicking router Vue links would always show urls like
#      (e.g.) localhost:8080/static/gen/repos/1
#      - However, upon page refresh, that url request would give 404
#   2. index.html file generated <script> tags that successfully find scripts
#      under (e.g.) /static/gen/js/app.js  - not sure how they were found
#      successfully because I don't think flask knows about that route, but
#      I'm guessing a request was passed through Flask and handled by Vue).
#      (e.g.) localhost:8080/static/gen/js/app.js
#
# To resolve #1 I removed `publicPath: '/static/gen'` from vue.config.js.
# That broke #2 because index.html now generates scripts as
# (e.g.) localhost:8080/js/app.js.
# The below two functions solve item #2, so now we respond to requests to
# /js/<file> with the proper file from the directory tree.

@root_api_blueprint.route('/js/<path:u_path>')
def get_javascript(u_path):
    return app.send_static_file('gen/js/{}'.format(u_path))


@root_api_blueprint.route('/css/<path:u_path>')
def get_css(u_path):
    return app.send_static_file('gen/css/{}'.format(u_path))


@root_api_blueprint.route('/favicon.ico')
def get_favicon():
    return app.send_static_file('gen/favicon.ico')
