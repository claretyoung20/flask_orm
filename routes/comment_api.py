from flask import request, jsonify, Blueprint

from models.schema import CommentSchema
from utilities import db
from models.comment import Comment

comment_app = Blueprint('comment_app', __name__)


# Create a new comment
@comment_app.route('/comments', methods=['POST'])
def create_comment():
    try:
        data = request.json
        new_comment = Comment(**data)
        db.session.add(new_comment)
        db.session.commit()
        comment_schema = CommentSchema()
        return jsonify(comment_schema.dump(new_comment)), 201
    except Exception as e:

        error = 500

        if isinstance(e.code, int):
            error = e.code

        return jsonify({'error': 'Internal Server Error'}), error


# Get all comments
@comment_app.route('/comments', methods=['GET'])
def get_comments():
    try:
        comments = Comment.query.all()
        comment_schema = CommentSchema(many=True)
        result = comment_schema.dump(comments)
        return jsonify(result)
    except Exception as e:
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


# Get a comment by ID
@comment_app.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    try:
        comment = Comment.query.get_or_404(comment_id)
        comment_schema = CommentSchema()
        result = comment_schema.dump(comment)
        return jsonify(result)
    except Exception as e:
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


# Update a comment by ID
@comment_app.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    try:
        comment = Comment.query.get_or_404(comment_id)
        data = request.json
        for key, value in data.items():
            setattr(comment, key, value)
        db.session.commit()
        return jsonify({'message': 'Comment updated successfully'})
    except Exception as e:
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


# Delete a comment by ID
@comment_app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted successfully'})
    except Exception as e:
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


# if __name__ == '__main__':
#     comment_app.run(debug=True)
