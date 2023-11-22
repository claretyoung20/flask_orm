from flask import request, jsonify, Blueprint

from models.schema import UserSchema, PostSchema, CommentSchema
from routes import log_error
from utilities import db
from models.comment import Comment
from models.post import Post
from models.user import User


post_app = Blueprint('post_app', __name__)


@post_app.route('/posts', methods=['POST'])
def create_post():
    try:
        data = request.json
        new_post = Post(**data)
        db.session.add(new_post)
        db.session.commit()
        post_schema = PostSchema()
        return jsonify(post_schema.dump(new_post)), 201
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


# Get all posts
@post_app.route('/posts', methods=['GET'])
def get_posts():
    try:
        posts = Post.query.all()
        post_schema = PostSchema(many=True)
        result = post_schema.dump(posts)
        return jsonify(result)
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


@post_app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        post_schema = PostSchema()
        result = post_schema.dump(post)
        return jsonify(result)
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


@post_app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        data = request.json
        for key, value in data.items():
            setattr(post, key, value)
        db.session.commit()
        return jsonify({'message': 'Post updated successfully'})
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


@post_app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'})
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


@post_app.route('/posts/<int:post_id>/comments2', methods=['GET'])
def get_comments_for_post2(post_id):
    try:
        comments = Comment.query.filter_by(post_id=post_id).all()

        comment_schema = CommentSchema(many=True)
        comment_data = comment_schema.dump(comments)

        return jsonify(comment_data)
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


@post_app.route('/posts/<int:post_id>/commented_users', methods=['GET'])
def get_users_who_commented(post_id):
    try:
        users = User.query.join(Comment, User.id == Comment.user_id).filter(Comment.post_id == post_id).all()
        user_schema = UserSchema(many=True)
        result = user_schema.dump(users)
        return jsonify(result)
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


