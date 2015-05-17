from server import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(30), unique=True, index=True)
    name = db.Column(db.String(80))

    def __init__(self, name, google_id):
        self.name = name
        self.google_id = google_id