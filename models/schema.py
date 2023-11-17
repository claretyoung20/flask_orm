from marshmallow import fields
from models.comment import Comment
from models.post import Post
from models.user import User
from utilities import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post


class CommentSchema(ma.SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema)

    class Meta:
        model = Comment
