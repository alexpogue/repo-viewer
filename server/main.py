import repo_viewer

app = repo_viewer.create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
