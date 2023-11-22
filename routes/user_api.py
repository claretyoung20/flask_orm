from flask import request, jsonify, Blueprint, Flask

from models.schema import UserSchema
from routes import log_error
from utilities import db
from models.user import User

user_app = Blueprint('user_app', __name__)


@user_app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.json
        create_new_user = User(**data)
        db.session.add(create_new_user)
        db.session.commit()
        user_schema = UserSchema()
        new_user = user_schema.dump(create_new_user)
        return jsonify(new_user), 201
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


@user_app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        user_schema = UserSchema(many=True)
        result = user_schema.dump(users)
        return jsonify(result)
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


@user_app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        user_schema = UserSchema()
        result = user_schema.dump(user)
        return jsonify(result)
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


@user_app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error


@user_app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        log_error(e)
        error = 500
        if e.code:
            error = e.code
        return jsonify({'error': e.description}), error
