# Repo Viewer

Viewer for the most-starred Github Python repositories in the world.

### Setup

Install Python 3.9 (I tested with 3.9.4)
Install [Google SDK Command Line Tools](https://cloud.google.com/sdk).

### Config.py

Add a `config.py` file to the `server` directory with the following contents:

```
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Sqlite for local testing
# SQLALCHEMY_DATABASE_URI = "sqlite:///repo_store.db"

# Google cloud sql when hosted locally
# SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://<user>:<password>@<postgres_host>:<postgres_port>/<db_name>"

# Google cloud sql when hosted on google appengine
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://<user>:<password>@/<db_name>?host=/cloudsql/<connection_name_from_app_engine_sql_overview>"

GITHUB_APP_ID = '<github_app_id>'
GITHUB_APP_CLIENT_ID = '<github_app_client_id>'
GITHUB_APP_CLIENT_SECRET = '<github_app_client_secret>'
```

Before deploying to different environments, I would comment and uncomment the
appropriate SQL line. Going forward, this config change should probably happen
automatically during the build process.

### Building production client

The final app is fully contained in the `server` directory. But first we need to build the client and copy it into the `server` subdirectories. Here's how:

* `cd client`
* `npm run prod`
* `cd ..`

### Running the server locally

After you have built the production client above, run the server with these commmands:

* `cd server`
* `pipenv lock -r > requirements.txt`
* `dev_appserver.py app.yaml`

### Viewing the running app

The `dev_appserver.py`'s output should have a `Listening at: http://<url>:<port>`. Copy the `http:://<url>:<port>` part to a web browser to see it running.


### Pushing to Google Cloud

Once the build process above is completed, we can now push the app to Google Cloud. To do this, run this from the server directory:

`gcloud app deploy app.yaml`

When the command completes, run `gcloud app browse` to see it running.


## Architecture

### Stack

* Frontend: Vue.js, Vuex for state, and styled with bootstrap
* Backend: Python using Flask, SQLAlchemy for database, marshmallow for
  database serialization/deserialization
* Database: Postgresql hosted on Google App Engine
* Server host: Google App Engine

### How it works

The main page of the app shows a list of repositories, and buttons to
authenticate to Github and refresh the list.

Each repository in the list is clickable and gives additional details.

The button first encourages you to Authenticate to Github. After
authenticating, the button changes to "Refresh database" and the Github token
is shown.

Upon clicking "Refresh database", a status message appears underneath so the
user knows the backend status.

When database refresh is complete, the list automatically updates with the new
values in the "Stars" column and keeps itself sorted by star count.

### Why authenticate with Github?

By default Github rate limits you after only 50 API calls. Refreshing the
database requires one API call for each repository, so that's 31 API calls per
update. So we can do less than 2 updates before we hit the API limit.

Authenticating with a Github app increases this limit to 5000 API calls.

### Secret sauce

I wanted to be sure that after loading the list of repositories, the page would
never have to call the API again. To do this, I introduced Vuex to keep track
of the list of repositories even during page navigation. That is why after
loading the main page, you can quickly click into and out of a repo without any
loading.

### Technical challenges

I hit multiple significant technical challenges:
  1. Discovering rate limits, deciding to do Github authentication, and then
     figuring out how to do it.
  2. Hosting a Vue.js app from Flask
     * Flask wanted to handle routing, so I needed to add a "catch-all" Flask
       route that routed any unknown routes to Vue's index.
     * I needed a place to host the files for Vue inside the Flask App. This is
       also important for Google App Engine hosting. After a lot of digging, I
       decided on two directories in my project: `server` for the Flask app and
       `client` for Vue.js. Vue's build process then builds the `client` code
       and puts it into Flask project's `static/gen` and `templates/gen`
       folders where Flask can find them. After few Vue build config changes,
       we're up and running.
     * The app started successfully after the above changes, and links seemed
       to work. However, clicking a link changed the url to
       `localhost:8080/static/gen/repos/1` when I instead wanted
       `localhost:8080/repos/1`. To resolve this issue, I removed the
       `publicPath: /static/gen` from the vue.config.js. This broke the
       generated `<script>` and `<style>` tag links which use the `publicPath`
       to determine location of js and css files which are under
       `static/gen/js`and `static/gen/css`, respectively. As a workaround, I
       added a Flask catch-all under `/js` and `/css` routes to route to the
       proper `static/gen` requests on the server.
