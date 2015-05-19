from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from server import db


following_association = db.Table('following_association', db.Model.metadata,
                                       db.Column('following', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                                       db.Column('followed', db.Integer, db.ForeignKey('users.id'), primary_key=True)
                                       )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(30), unique=True, index=True)
    name = db.Column(db.String(80))
    following = relationship('User',
                             secondary=following_association,
                             primaryjoin=(id == following_association.c.following),
                             secondaryjoin=(id == following_association.c.followed),
                             backref='followers')

    def __init__(self, name, google_id):
        self.name = name
        self.google_id = google_id