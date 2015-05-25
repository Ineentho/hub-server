import datetime
from sqlalchemy.exc import IntegrityError
from server import db
from server.util import hash_password, verify_password


class ChannelExistsError(Exception):
    pass


class ChannelNotFoundError(Exception):
    pass


class IncorrectPasswordError(Exception):
    pass


class SlugExistsError(Exception):
    pass


def authenticate_channel(slug, password):
    channel = Channel.query.filter_by(slug=slug).first()

    if not channel:
        raise ChannelNotFoundError()

    if not verify_password(channel.password, password):
        raise IncorrectPasswordError()

    return channel


def create_channel(name, slug, url, password, hosted_by):
    channel = Channel(name, slug, url, password, hosted_by)

    db.session.add(channel)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ChannelExistsError(e)
    pass


def post_video(channel, slug, name):
    video = Video(slug, name)
    channel.videos.append(video)
    db.session.add(channel)

    try:
        db.session.commit()
    except IntegrityError as e:
        raise SlugExistsError(e)


class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    slug = db.Column(db.String(80), unique=True)
    hosted_by = db.Column(db.String(80))
    url = db.Column(db.String(256))
    password = db.Column(db.LargeBinary(256), unique=True)
    videos = db.relationship('Video', backref='channel')

    def __init__(self, name, slug, url, password, hosted_by):
        self.name = name
        self.password = hash_password(password)
        self.url = url
        self.slug = slug
        self.hosted_by = hosted_by


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    slug = db.Column(db.String(80))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    comments = db.relationship('Comment', backref='videos')

    __table_args__ = (db.UniqueConstraint('slug', 'channel_id', name='_video_slug_uc'),)

    def __init__(self, slug, name):
        self.name = name
        self.slug = slug


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1024))
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
    video = db.relationship('Video')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, comment, user, video):
        self.comment = comment
        self.user_id = user.id
        self.video_id = video.id


class FeedItem(db.Model):
    __tablename__ = 'feed'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Backref'd as user
    event_type = db.Column(db.Integer)  # See init function
    like_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
    like = db.relationship('Video')
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    comment = db.relationship('Comment')
    date = db.Column(db.DateTime)

    def __init__(self, user, event_type, item):
        self.event_type = event_type
        self.user_id = user.id
        self.date = datetime.datetime\
            .now()

        if event_type == 0:
            # Like
            self.like_id = item.id
        elif event_type == 1:
            # Comment
            print(item.id)
            self.comment_id = item.id
