# Repo Viewer

Viewer for the most-starred Github Python repositories in the world.

### Setup

Install Python 3.9 (I tested with 3.9.4)
Install [Google SDK Command Line Tools](https://cloud.google.com/sdk).

### Building production client

The final app is fully contained in the `server` directory. But first we need to build the client and copy it into the `server` subdirectories. Here's how:

`cd client`
`npm run prod`
`cd ..`

### Running the server locally

After you have built the production client above, run the server with these commmands:

`cd server`
`pipenv lock -r > requirements.txt`
`dev_appserver.py app.yaml`

### Viewing the running app

The `dev_appserver.py`'s output should have a `Listening at: http://<url>:<port>`. Copy the `http:://<url>:<port>` part to a web browser to see it running.


### Pushing to Google Cloud

Once the build process above is completed, we can now push the app to Google Cloud. To do this, run this from the server directory:

`gcloud app deploy app.yaml`

When the command completes, run `gcloud app browse` to see it running.
