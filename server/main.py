import repo_viewer
import os

app = repo_viewer.create_app()

if __name__ == '__main__':
    # Google AppEngine sets PORT env var to specify  port it wants us to run on
    PORT = os.environ.get('PORT')
    if PORT is not None:
        app.run(host='0.0.0.0', port=PORT)
    else:
        app.run(host='0.0.0.0')
