import sys
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from server.util import UnbufferedStream

# Disable all output buffering (Some messages doesn't display in docker otherwise)
sys.stdout = UnbufferedStream(sys.stdout)


db = None
app = None


def get_db():
    return db


def create_app(config):
    global app
    if app:
        return app
    app = Flask(__name__)
    for k in config:
        app.config[k] = config[k]
    load_db()
    return app


def load_db():
    global db
    global app

    db = SQLAlchemy(app)

    # Register all APIs
    import server.auth
    import server.api_public
    import server.api_channel
    print('apps imported')

    db.create_all()
    db.session.commit()
