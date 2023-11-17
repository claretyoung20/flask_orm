from utilities import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    address = db.Column(db.String(100))
    profile_image_url = db.Column(db.String(255))
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', back_populates='user', lazy=True)
