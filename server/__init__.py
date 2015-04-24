import sys
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from server.util import UnbufferedStream

# Disable all output buffering (Some messages doesn't display in docker otherwise)
sys.stdout = UnbufferedStream(sys.stdout)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@db:5432/'


def load():
    global db
    db = SQLAlchemy(app)

    # Register all APIs
    import server.auth
    import server.api_public
    import server.api_channel

    db.create_all()


def recreate_db():
    db.drop_all()
    db.create_all()