from utilities import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user = db.relationship('User', back_populates='comments', lazy=True, foreign_keys=[user_id])
