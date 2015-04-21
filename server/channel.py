from sqlalchemy.exc import IntegrityError
from server import db
from server.util import hash_password


class ChannelExistsError(Exception):
    pass


def create_channel(name, slug, url, password):
    channel = Channel(name, slug, url, password)
    db.session.add(channel)

    try:
        db.session.commit()
    except IntegrityError as e:
        raise ChannelExistsError(e)
    pass

def post_video(channel, name, slug):
    db.session.query()


class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    slug = db.Column(db.String(80), unique=True)
    url = db.Column(db.String(256))
    password = db.Column(db.Binary(256), unique=True)
    videos = db.relationship('Video')

    def __init__(self, name, slug, url, password):
        self.name = name
        self.password = hash_password(password)
        self.url = url
        self.slug = slug


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    slug = db.Column(db.String(80), unique=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug